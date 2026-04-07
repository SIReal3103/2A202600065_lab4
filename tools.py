import json
from langchain_core.tools import tool

# ============================================================
# MOCK DATA - Dữ liệu hệ thống
# ============================================================
FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Melia", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}

# ============================================================
# TOOL IMPLEMENTATIONS
# ============================================================

@tool
def search_flights(origin: str, destination: str) -> str:
    """Tra cứu chuyến bay. Có xử lý tra cứu ngược nếu không tìm thấy chiều đi."""
    ori, dest = origin.strip(), destination.strip()
    
    flights = FLIGHTS_DB.get((ori, dest))
    prefix = ""
    
    if not flights:
        flights = FLIGHTS_DB.get((dest, ori))
        if flights:
            prefix = f"[LƯU Ý: Không có chuyến {ori}->{dest}, dưới đây là chuyến ngược lại {dest}->{ori}]\n"
            
    if not flights:
        return f"Không tìm thấy chuyến bay từ {ori} đến {dest}."
    
    res = [f"- {f['airline']} ({f['class']}): {f['departure']}->{f['arrival']} | Giá: {f['price']:,}đ".replace(",", ".") for f in flights]
    return prefix + "\n".join(res)

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """Tìm khách sạn, tự động lọc theo giá tối đa và sắp xếp theo Rating giảm dần."""
    hotels = HOTELS_DB.get(city.strip())
    if not hotels:
        return f"Không tìm thấy dữ liệu khách sạn tại thành phố {city}."
    
    filtered = [h for h in hotels if h['price_per_night'] <= max_price_per_night]
    filtered.sort(key=lambda x: x['rating'], reverse=True)
    
    if not filtered:
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {max_price_per_night:,}đ/đêm. Hãy thử tăng ngân sách.".replace(",", ".")
        
    res = [f"- {h['name']} ({h['stars']}⭐) | Giá: {h['price_per_night']:,}đ/đêm | Khu vực: {h['area']} | Rating: {h['rating']}".replace(",", ".") for h in filtered]
    return "\n".join(res)

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """Tính ngân sách. Phân tách chuỗi expenses an toàn với try/except."""
    try:
        total_spent = 0
        details = []
        
        items = [i.strip() for i in expenses.split(',')]
        for item in items:
            name, price = item.split(':')
            price_val = int(price.strip())
            total_spent += price_val
            details.append(f"- {name.strip().capitalize()}: {price_val:,}đ".replace(",", "."))
            
        remaining = total_budget - total_spent
        
        report = "Bảng chi phí:\n" + "\n".join(details)
        report += "\n---------------------"
        report += f"\nTổng chi: {total_spent:,}đ".replace(",", ".")
        report += f"\nNgân sách: {total_budget:,}đ".replace(",", ".")
        report += f"\nCòn lại: {remaining:,}đ".replace(",", ".")
        
        if remaining < 0:
            report += f"\n⚠️ Vượt ngân sách {abs(remaining):,}đ! Cần điều chỉnh.".replace(",", ".")
            
        return report
        
    except ValueError:
        return "Lỗi tính toán: Số tiền không hợp lệ. Hãy đảm bảo định dạng là 'tên:số_tiền'."
    except Exception as e:
        return f"Lỗi xử lý dữ liệu expenses: {str(e)}. Định dạng chuẩn: 'vé máy bay:890000, khách sạn:650000'."