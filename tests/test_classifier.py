from rule_engine.classifier import classify

def test_r01_phan_ve():
    res = classify({
        "tuoi": 25,
        "huyet_ap_tam_thu": 110,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R01-PV"


def test_r02_phan_ve():
    res = classify({
        "tuoi": 10,
        "huyet_ap_tam_thu": 100,
        "co_di_nguyen_nghi_ngo": True,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_tieu_hoa_nang": True,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R02-PV"


def test_r03_phan_ve():
    res = classify({
        "tuoi": 5,
        "huyet_ap_tam_thu": 95,
        "co_di_nguyen_nghi_ngo": True,
        "di_nguyen_qua_duong_hit": False,
        "co_trieu_chung_ho_hap": True,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R03-PV"


def test_soc_phan_ve_tuoi_tre_em_bien():
    res = classify({
        "tuoi": 5,
        "huyet_ap_tam_thu": 79,
        "co_di_nguyen_nghi_ngo": True,
        "co_trieu_chung_tuan_hoan": True,
    })
    assert res["muc_do"] == "SOC_PHAN_VE"
    assert res["rule_id"] == "R-SOC"


def test_soc_phan_ve_giam_30_phan_tram():
    res = classify({
        "tuoi": 30,
        "huyet_ap_tam_thu": 95,
        "huyet_ap_tam_thu_nen": 140,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_tuan_hoan": True,
    })
    assert res["muc_do"] == "SOC_PHAN_VE"
    assert res["rule_id"] == "R-SOC"


def test_thieu_tuoi_tra_ve_theo_doi():
    res = classify({
        "co_di_nguyen_nghi_ngo": True,
        "co_trieu_chung_tuan_hoan": True,
    })
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


# ==========================================
# CÁC TEST MỚI BỔ SUNG CHO M2 (CHECKPOINT 2)
# ==========================================

def test_boundary_tuoi_so_sinh():
    # Tuổi 0.5 (dưới 1 tuổi), HATT 69 < 70 -> Sốc phản vệ
    res = classify({
        "tuoi": 0.5,
        "huyet_ap_tam_thu": 69,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
    })
    assert res["muc_do"] == "SOC_PHAN_VE"
    assert res["rule_id"] == "R-SOC"


def test_invalid_tuoi_am():
    res = classify({
        "tuoi": -5,
        "co_di_nguyen_nghi_ngo": True
    })
    assert res["muc_do"] == "THEO_DOI"
    assert "Thieu hoac sai thong tin tuoi" in res["ly_do"]


def test_invalid_input_khong_phai_dict():
    res = classify(None)  # type: ignore
    assert res["muc_do"] == "THEO_DOI"
    assert "khong hop le" in res["ly_do"]


def test_missing_input_rong():
    res = classify({})
    assert res["muc_do"] == "THEO_DOI"
    assert "Thieu hoac sai thong tin tuoi" in res["ly_do"]


def test_audit_trail_khong_chua_pii():
    # Test này yêu cầu đã dán hàm classify_and_audit() vào cuối file classifier.py
    from rule_engine.classifier import classify_and_audit
    import os
    
    # Xóa log cũ nếu có để test môi trường sạch
    if os.path.exists('audit.log'):
        os.remove('audit.log')
        
    res = classify_and_audit({"tuoi": 25}, "test-uuid-1234")
    assert res["muc_do"] == "THEO_DOI"
    
    with open('audit.log', 'r') as f:
        log_content = f.read()
    
    # Đảm bảo có đủ 4 trường bắt buộc
    assert "Timestamp" in log_content
    assert "test-uuid-1234" in log_content
    assert "CLASSIFY_ANAPHYLAXIS" in log_content
    assert "THEO_DOI" in log_content
    
    # Đảm bảo KHÔNG log PII hoặc triệu chứng
    assert "tuoi" not in log_content