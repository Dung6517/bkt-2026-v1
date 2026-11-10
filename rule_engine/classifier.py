"""Rule Engine WAO/EAACI - khung bai tap BKT-1 (Track A), mon KTPMUD.

Sinh vien hien thuc ham classify() theo dac ta trong docs/decision-table.md.
KHONG tu dat nguong/quy tac moi chua co trong dac ta.
"""
from __future__ import annotations

import datetime
import json
from typing import Any, Dict, Optional, TypedDict


class PatientInput(TypedDict, total=False):
    """Input theo dung Data Dictionary trong docs/decision-table.md."""
    tuoi: float
    huyet_ap_tam_thu: Optional[int]
    huyet_ap_tam_thu_nen: Optional[int]
    co_di_nguyen_nghi_ngo: bool
    di_nguyen_qua_duong_hit: bool
    co_ton_thuong_da_niem_mac: bool
    co_trieu_chung_ho_hap: bool
    co_trieu_chung_tuan_hoan: bool
    co_trieu_chung_tieu_hoa_nang: bool


class ClassificationResult(TypedDict):
    muc_do: str  # "SOC_PHAN_VE" | "PHAN_VE" | "THEO_DOI" - dung dung nhan theo docs/decision-table.md
    rule_id: Optional[str]  # "R-SOC" | "R01-PV" | "R02-PV" | "R03-PV" | None
    ly_do: str


def _is_hypotension(
    tuoi: float,
    hatt: Optional[int],
    hatt_nen: Optional[int],
) -> bool:
    """Kiem tra tieu chi tut huyet ap tam thu theo nhom tuoi (Tang 1)."""
    if hatt is None or not isinstance(hatt, (int, float)) or isinstance(hatt, bool) or hatt < 0:
        return False

    if 0 <= tuoi < 1:
        return hatt < 70
    if 1 <= tuoi < 11:
        return hatt < (70 + 2 * tuoi)
    if 11 <= tuoi < 18:
        return hatt < 90
    if tuoi >= 18:
        if hatt < 90:
            return True
        if (
            hatt_nen is not None
            and isinstance(hatt_nen, (int, float))
            and not isinstance(hatt_nen, bool)
            and hatt_nen > 0
        ):
            return (hatt_nen - hatt) / hatt_nen > 0.30
    return False


def classify(patient: PatientInput) -> ClassificationResult:
    """Phan loai muc do theo docs/decision-table.md."""
    if not isinstance(patient, dict):
        return {
            "muc_do": "THEO_DOI",
            "rule_id": None,
            "ly_do": "Du lieu dau vao khong hop le.",
        }

    tuoi = patient.get("tuoi")
    if tuoi is None or not isinstance(tuoi, (int, float)) or isinstance(tuoi, bool) or tuoi < 0:
        return {
            "muc_do": "THEO_DOI",
            "rule_id": None,
            "ly_do": "Thieu hoac sai thong tin tuoi, chua du du kien ket luan.",
        }

    di_nguyen = bool(patient.get("co_di_nguyen_nghi_ngo", False))
    qua_duong_hit = bool(patient.get("di_nguyen_qua_duong_hit", False))
    da_niem_mac = bool(patient.get("co_ton_thuong_da_niem_mac", False))
    ho_hap = bool(patient.get("co_trieu_chung_ho_hap", False))
    tuan_hoan = bool(patient.get("co_trieu_chung_tuan_hoan", False))
    tieu_hoa = bool(patient.get("co_trieu_chung_tieu_hoa_nang", False))

    # Tang 2: Kiem tra 3 kich ban Phan ve
    matched_rule: Optional[str] = None
    if not di_nguyen and da_niem_mac and (ho_hap or tuan_hoan):
        matched_rule = "R01-PV"
    elif di_nguyen and (da_niem_mac + ho_hap + tuan_hoan + tieu_hoa) >= 2:
        matched_rule = "R02-PV"
    elif di_nguyen and ((not qua_duong_hit and ho_hap) or tuan_hoan):
        matched_rule = "R03-PV"

    if matched_rule is None:
        return {
            "muc_do": "THEO_DOI",
            "rule_id": None,
            "ly_do": "Chua du tieu chi chan doan phan ve theo bang quyet dinh.",
        }

    # Tang 1: Kiem tra Soc phan ve
    hatt = patient.get("huyet_ap_tam_thu")
    hatt_nen = patient.get("huyet_ap_tam_thu_nen")

    if _is_hypotension(tuoi, hatt, hatt_nen):
        return {
            "muc_do": "SOC_PHAN_VE",
            "rule_id": "R-SOC",
            "ly_do": f"Dat tieu chi phan ve ({matched_rule}) kem tut huyet ap theo tuoi.",
        }

    return {
        "muc_do": "PHAN_VE",
        "rule_id": matched_rule,
        "ly_do": f"Dat tieu chi phan ve theo kich ban {matched_rule}.",
    }


def classify_and_audit(
    patient: PatientInput,
    user_uuid: str,
    log_path: str = "audit.log",
) -> ClassificationResult:
    """Goi classify() va ghi log audit 4 truong (Tieu chi A-06)."""
    result = classify(patient)

    audit_entry: Dict[str, Any] = {
        "Timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "User_UUID": user_uuid,
        "Action_Type": "CLASSIFY_ANAPHYLAXIS",
        "Status": result["muc_do"],
    }
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(audit_entry, ensure_ascii=False) + "\n")

    return result