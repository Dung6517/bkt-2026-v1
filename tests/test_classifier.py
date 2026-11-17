import json
from pathlib import Path
from rule_engine.classifier import classify, classify_and_audit


# ==========================================
# 1. NHÓM NORMAL (TC-N01 -> TC-N06)
# ==========================================

def test_tc_n01_r01_phan_ve():
    res = classify({
        "tuoi": 25,
        "huyet_ap_tam_thu": 115,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R01-PV"


def test_tc_n02_r02_phan_ve():
    res = classify({
        "tuoi": 30,
        "huyet_ap_tam_thu": 110,
        "co_di_nguyen_nghi_ngo": True,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_tieu_hoa_nang": True,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R02-PV"


def test_tc_n03_r03_phan_ve():
    res = classify({
        "tuoi": 10,
        "huyet_ap_tam_thu": 95,
        "co_di_nguyen_nghi_ngo": True,
        "di_nguyen_qua_duong_hit": False,
        "co_trieu_chung_ho_hap": True,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R03-PV"


def test_tc_n04_soc_phan_ve():
    res = classify({
        "tuoi": 35,
        "huyet_ap_tam_thu": 80,
        "co_di_nguyen_nghi_ngo": True,
        "co_trieu_chung_tuan_hoan": True,
    })
    assert res["muc_do"] == "SOC_PHAN_VE"
    assert res["rule_id"] == "R-SOC"


def test_tc_n05_theo_doi():
    res = classify({
        "tuoi": 22,
        "huyet_ap_tam_thu": 120,
        "co_di_nguyen_nghi_ngo": True,
        "co_ton_thuong_da_niem_mac": True,
    })
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_tc_n06_uu_tien_r02_over_r03():
    # Khớp đồng thời R02-PV và R03-PV -> phải ưu tiên R02-PV
    res = classify({
        "tuoi": 28,
        "huyet_ap_tam_thu": 110,
        "co_di_nguyen_nghi_ngo": True,
        "di_nguyen_qua_duong_hit": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R02-PV"


# ==========================================
# 2. NHÓM BOUNDARY (TC-B01 -> TC-B06)
# ==========================================

def test_tc_b01_tre_duoi_1_tuoi_tut_hatt():
    res = classify({
        "tuoi": 0.5,
        "huyet_ap_tam_thu": 69,
        "co_di_nguyen_nghi_ngo": True,
        "co_trieu_chung_tuan_hoan": True,
    })
    assert res["muc_do"] == "SOC_PHAN_VE"
    assert res["rule_id"] == "R-SOC"


def test_tc_b02_tre_duoi_1_tuoi_bang_nguong_70():
    res = classify({
        "tuoi": 0.5,
        "huyet_ap_tam_thu": 70,
        "co_di_nguyen_nghi_ngo": True,
        "co_trieu_chung_tuan_hoan": True,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R03-PV"


def test_tc_b03_tre_1_den_duoi_11_tuoi_tut_hatt():
    # Ngưỡng 70 + 2*5 = 80 -> HATT 79 < 80 -> SOC_PHAN_VE
    res = classify({
        "tuoi": 5,
        "huyet_ap_tam_thu": 79,
        "co_di_nguyen_nghi_ngo": True,
        "co_trieu_chung_tuan_hoan": True,
    })
    assert res["muc_do"] == "SOC_PHAN_VE"
    assert res["rule_id"] == "R-SOC"


def test_tc_b04_tre_11_den_duoi_18_tuoi_tut_hatt():
    res = classify({
        "tuoi": 11,
        "huyet_ap_tam_thu": 89,
        "co_di_nguyen_nghi_ngo": True,
        "co_trieu_chung_tuan_hoan": True,
    })
    assert res["muc_do"] == "SOC_PHAN_VE"
    assert res["rule_id"] == "R-SOC"


def test_tc_b05_giam_dung_30_phan_tram_khong_soc():
    # (130 - 91) / 130 = 30.0% -> không tính tụt huyết áp (> 30%)
    res = classify({
        "tuoi": 18,
        "huyet_ap_tam_thu": 91,
        "huyet_ap_tam_thu_nen": 130,
        "co_di_nguyen_nghi_ngo": True,
        "co_trieu_chung_tuan_hoan": True,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R03-PV"


def test_tc_b06_giam_hon_30_phan_tram_soc():
    # (130 - 90) / 130 = 30.77% > 30% -> SOC_PHAN_VE
    res = classify({
        "tuoi": 18,
        "huyet_ap_tam_thu": 90,
        "huyet_ap_tam_thu_nen": 130,
        "co_di_nguyen_nghi_ngo": True,
        "co_trieu_chung_tuan_hoan": True,
    })
    assert res["muc_do"] == "SOC_PHAN_VE"
    assert res["rule_id"] == "R-SOC"


# ==========================================
# 3. NHÓM MISSING (TC-M01 -> TC-M04)
# ==========================================

def test_tc_m01_thieu_key_tuoi():
    res = classify({
        "co_di_nguyen_nghi_ngo": True,
        "co_trieu_chung_tuan_hoan": True,
    })
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_tc_m02_tuoi_null():
    res = classify({
        "tuoi": None,  # type: ignore
        "co_di_nguyen_nghi_ngo": True,
        "co_trieu_chung_tuan_hoan": True,
    })
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_tc_m03_thieu_hatt_van_xet_tang_2():
    res = classify({
        "tuoi": 25,
        "huyet_ap_tam_thu": None,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R01-PV"


def test_tc_m04_thieu_cac_khoa_bool_mac_dinh_false():
    res = classify({
        "tuoi": 25,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R01-PV"


# ==========================================
# 4. NHÓM INVALID (TC-I01 -> TC-I04 + Non-dict)
# ==========================================

def test_tc_i01_input_rong():
    res = classify({})
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_tc_i02_tuoi_am():
    res = classify({
        "tuoi": -1,
        "huyet_ap_tam_thu": 100,
        "co_di_nguyen_nghi_ngo": True,
        "co_trieu_chung_tuan_hoan": True,
    })
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_tc_i03_hatt_am_bo_qua_tang_1():
    res = classify({
        "tuoi": 25,
        "huyet_ap_tam_thu": -50,
        "co_di_nguyen_nghi_ngo": True,
        "co_trieu_chung_tuan_hoan": True,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R03-PV"


def test_tc_i04_sai_kieu_du_lieu_tuoi():
    res = classify({
        "tuoi": "hai mươi",  # type: ignore
        "huyet_ap_tam_thu": 100,
    })
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_invalid_input_khong_phai_dict():
    res = classify(None)  # type: ignore
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


# ==========================================
# 5. AUDIT TRAIL & EXPLAINABILITY (A-05, A-06)
# ==========================================

def test_audit_trail_4_truong_va_khong_loi_khuyen_dieu_tri(tmp_path: Path):
    log_file = tmp_path / "audit_test.log"
    res = classify_and_audit(
        {
            "tuoi": 25,
            "huyet_ap_tam_thu": 115,
            "co_di_nguyen_nghi_ngo": False,
            "co_ton_thuong_da_niem_mac": True,
            "co_trieu_chung_ho_hap": True,
        },
        user_uuid="test-uuid-1234",
        log_path=str(log_file),
    )
    assert res["muc_do"] == "PHAN_VE"
    assert "R01-PV" in res["ly_do"]
    assert "adrenalin" not in res["ly_do"].lower()
    assert "tiêm" not in res["ly_do"].lower()

    entry = json.loads(log_file.read_text(encoding="utf-8").strip())
    assert list(entry.keys()) == ["Timestamp", "User_UUID", "Action_Type", "Status"]
    assert entry["User_UUID"] == "test-uuid-1234"
    assert entry["Action_Type"] == "CLASSIFY_ANAPHYLAXIS"
    assert entry["Status"] == "PHAN_VE"