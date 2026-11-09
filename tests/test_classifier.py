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