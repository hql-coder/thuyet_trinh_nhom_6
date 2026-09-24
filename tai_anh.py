import requests
import os
import time

# ============ CẤU HÌNH ============
PEXELS_API_KEY = "DÁN_API_KEY_CỦA_BẠN_VÀO_ĐÂY"  # ← Thay key của bạn
THU_MUC_LUU = "images"
SO_ANH_MOI_TU_KHOA = 3  # Tải 3 ảnh mỗi từ khóa để chọn ảnh đẹp nhất

# Danh sách ảnh cần tải (tên file + từ khóa tìm kiếm)
DANH_SACH_ANH = {
    "bia.jpg": "students holding hands unity",
    "dinh_nghia.jpg": "students discussion classroom",
    "thuc_trang.jpg": "lonely student hallway",
    "hinh_thuc.jpg": "stop sign hand gesture",
    "gia_dinh.jpg": "happy family together",
    "nha_truong.jpg": "teacher students classroom",
    "ban_than.jpg": "thoughtful student window",
    "hau_qua_1.jpg": "sad student alone",
    "hau_qua_2.jpg": "students standing together",
    "giai_phap_1.jpg": "school assembly presentation",
    "giai_phap_2.jpg": "students playing sports school",
    "giai_phap_3.jpg": "parents teachers meeting school",
    "vai_tro.jpg": "student raising hand classroom",
    "ket_thuc.jpg": "happy students graduation",
}

# ============ HÀM TẢI ẢNH ============
def tim_anh_pexels(tu_khoa, so_luong=3):
    """Tìm ảnh trên Pexels theo từ khóa"""
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": tu_khoa,
        "per_page": so_luong,
        "orientation": "landscape",  # Ảnh ngang cho slide
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if "photos" in data and len(data["photos"]) > 0:
            # Trả về danh sách URL ảnh chất lượng lớn
            return [photo["src"]["large2x"] for photo in data["photos"]]
        else:
            print(f"  ⚠️ Không tìm thấy ảnh cho: {tu_khoa}")
            return []
    except Exception as e:
        print(f"  ❌ Lỗi API: {e}")
        return []

def tai_anh(url, duong_dan_luu):
    """Tải ảnh từ URL và lưu về máy"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(duong_dan_luu, "wb") as f:
            f.write(response.content)
        
        # Kiểm tra kích thước file
        kich_thuoc = os.path.getsize(duong_dan_luu) / 1024  # KB
        return True, kich_thuoc
    except Exception as e:
        print(f"  ❌ Lỗi tải: {e}")
        return False, 0

# ============ CHẠY CHÍNH ============
def main():
    # Tạo thư mục images
    os.makedirs(THU_MUC_LUU, exist_ok=True)
    
    print("=" * 60)
    print("🎨 TỰ ĐỘNG TẢI ẢNH CHO SLIDE BẠO LỰC HỌC ĐƯỜNG")
    print("=" * 60)
    
    # Kiểm tra API key
    if PEXELS_API_KEY == "DÁN_API_KEY_CỦA_BẠN_VÀO_ĐÂY":
        print("❌ Bạn chưa dán API key Pexels!")
        print("👉 Vào https://www.pexels.com/api/ để lấy key miễn phí")
        return
    
    thanh_cong = 0
    that_bai = 0
    
    for ten_file, tu_khoa in DANH_SACH_ANH.items():
        print(f"\n📸 Đang tìm: {ten_file}")
        print(f"   Từ khóa: '{tu_khoa}'")
        
        # Tìm ảnh
        danh_sach_url = tim_anh_pexels(tu_khoa, SO_ANH_MOI_TU_KHOA)
        
        if not danh_sach_url:
            that_bai += 1
            continue
        
        # Tải ảnh đầu tiên (chất lượng tốt nhất)
        duong_dan = os.path.join(THU_MUC_LUU, ten_file)
        ok, kich_thuoc = tai_anh(danh_sach_url[0], duong_dan)
        
        if ok:
            print(f"   ✅ Đã lưu: {duong_dan} ({kich_thuoc:.0f} KB)")
            thanh_cong += 1
        else:
            # Thử ảnh thứ 2 nếu ảnh 1 lỗi
            if len(danh_sach_url) > 1:
                print("   🔄 Thử ảnh khác...")
                ok, kich_thuoc = tai_anh(danh_sach_url[1], duong_dan)
                if ok:
                    print(f"   ✅ Đã lưu: {duong_dan} ({kich_thuoc:.0f} KB)")
                    thanh_cong += 1
                    continue
            that_bai += 1
        
        # Nghỉ 1 giây để tránh bị rate limit
        time.sleep(1)
    
    # Tổng kết
    print("\n" + "=" * 60)
    print(f"✅ Thành công: {thanh_cong}/14 ảnh")
    print(f"❌ Thất bại: {that_bai}/14 ảnh")
    print(f"📁 Ảnh đã lưu trong thư mục: {THU_MUC_LUU}/")
    print("=" * 60)
    
    if that_bai > 0:
        print("\n💡 Gợi ý:")
        print("   - Kiểm tra lại API key")
        print("   - Thử chạy lại (có thể bị rate limit tạm thời)")
        print("   - Tự tải ảnh thiếu từ https://www.pexels.com")

if __name__ == "__main__":
    main()
