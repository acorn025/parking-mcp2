# MCP Tool 응답 형식 문서

## search_nearby_parking 함수 응답 구조

### 기본 응답 형식

```json
{
  "parkings": [
    {
      "name": "주차장 이름",
      "address": "주차장 주소",
      "total_spots": 100,
      "available_spots": 15,
      "fee": "카테고리 정보",
      "distance": 250,
      "operating_info": { ... },
      "fee_info": { ... },
      "update_time": "2025-12-10 10:24:30",
      "notice": "안내 메시지"
    }
  ],
  "count": 5
}
```

### 에러 응답 형식

```json
{
  "error": "에러 메시지",
  "parkings": []
}
```

---

## 지역별 응답 구조

### 1. 서울 지역 응답 (완전한 정보)

```json
{
  "parkings": [
    {
      "name": "서울시청 주차장",
      "address": "서울 중구 세종대로 110",
      "total_spots": 1260,
      "available_spots": 507,
      "fee": "교통,지하철 > 지하철역 > 주차장",
      "distance": 62,
      "operating_info": {
        "operating_type": "시간제 운영",
        "status": "주차~20분까지 무료이용 가능",
        "weekday_start": "0000",
        "weekday_end": "2400",
        "weekend_start": "0000",
        "weekend_end": "2400",
        "holiday_start": "0000",
        "holiday_end": "2400"
      },
      "fee_info": {
        "is_paid": "유료",
        "night_paid": "야간 무료",
        "basic_fee": 430.0,
        "basic_hours": 5.0,
        "additional_fee": 430.0,
        "additional_hours": 5.0,
        "daily_max_fee": 30900.0,
        "period_fee": 176000
      },
      "update_time": "2025-12-10 10:24:30"
    }
  ],
  "count": 1
}
```

**서울 지역 필드 설명:**
- `total_spots`: 총 주차 대수 (정수)
- `available_spots`: 주차 가능 대수 (정수, 실시간)
- `operating_info`: 운영 시간 정보 (객체)
- `fee_info`: 요금 정보 (객체)
- `update_time`: 실시간 정보 업데이트 시간 (문자열)

---

### 2. 경기 지역 응답 (요금 및 운영시간)

```json
{
  "parkings": [
    {
      "name": "화성행궁",
      "address": "경기도 수원시 팔달구 화성행궁 159",
      "total_spots": 62,
      "available_spots": null,
      "fee": "교통,지하철 > 지하철역 > 주차장",
      "distance": 0,
      "operating_info": {
        "weekday_start": "00:00",
        "weekday_end": "23:59",
        "saturday_start": "00:00",
        "saturday_end": "23:59",
        "holiday_start": "00:00",
        "holiday_end": "23:59"
      },
      "fee_info": {
        "is_paid": "유료",
        "basic_time": 90,
        "basic_fee": 400,
        "additional_time": 10,
        "additional_fee": 600,
        "payment_method": "카드결제"
      }
    }
  ],
  "count": 1
}
```

**경기 지역 필드 설명:**
- `total_spots`: 총 주차 대수 (정수, 제공됨)
- `available_spots`: null (경기 API에 실시간 정보 없음)
- `operating_info`: 운영 시간 정보 (객체)
- `fee_info`: 요금 정보 (객체)

---

### 3. 기타 지역 응답 (기본 정보만)

```json
{
  "parkings": [
    {
      "name": "해운대역 주차장",
      "address": "부산 해운대구 우동 1378-95",
      "total_spots": null,
      "available_spots": null,
      "fee": "교통,지하철 > 지하철역 > 주차장",
      "distance": 0,
      "notice": "해당 지역은 기본 주차장 정보만 제공됩니다. 실시간 정보는 서울 지역에서, 요금 및 운영시간 정보는 서울/경기 지역에서 이용 가능합니다."
    }
  ],
  "count": 1
}
```

**기타 지역 필드 설명:**
- `total_spots`: null
- `available_spots`: null
- `notice`: 안내 메시지 (문자열)

---

## 필드 상세 설명

### 공통 필드

| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `name` | string | 주차장 이름 | "서울시청 주차장" |
| `address` | string | 주차장 주소 | "서울 중구 세종대로 110" |
| `total_spots` | integer \| null | 총 주차 대수 | 1260 (서울/경기만) |
| `available_spots` | integer \| null | 주차 가능 대수 | 507 (서울만) |
| `fee` | string | 카테고리 정보 | "교통,지하철 > 지하철역 > 주차장" |
| `distance` | integer | 거리 (미터) | 250 |

### operating_info 객체 (서울/경기)

| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `operating_type` | string | 운영 구분 (서울만) | "시간제 운영" |
| `status` | string | 운영 상태 (서울만) | "주차~20분까지 무료이용 가능" |
| `weekday_start` | string | 평일 운영 시작 | "0000" 또는 "00:00" |
| `weekday_end` | string | 평일 운영 종료 | "2400" 또는 "23:59" |
| `weekend_start` | string | 주말 운영 시작 (서울) | "0000" |
| `weekend_end` | string | 주말 운영 종료 (서울) | "2400" |
| `saturday_start` | string | 토요일 운영 시작 (경기) | "00:00" |
| `saturday_end` | string | 토요일 운영 종료 (경기) | "23:59" |
| `holiday_start` | string | 공휴일 운영 시작 | "0000" 또는 "00:00" |
| `holiday_end` | string | 공휴일 운영 종료 | "2400" 또는 "23:59" |

### fee_info 객체 (서울/경기)

| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `is_paid` | string | 유료 여부 | "유료" 또는 "무료" |
| `night_paid` | string | 야간 유료 여부 (서울만) | "야간 무료" |
| `basic_fee` | number | 기본 주차 요금 (원) | 430.0 |
| `basic_hours` | number | 기본 주차 시간 (분, 서울) | 5.0 |
| `basic_time` | number | 기본 주차 시간 (분, 경기) | 90 |
| `additional_fee` | number | 추가 주차 요금 (원) | 430.0 |
| `additional_hours` | number | 추가 주차 시간 (분, 서울) | 5.0 |
| `additional_time` | number | 추가 주차 시간 (분, 경기) | 10 |
| `daily_max_fee` | number | 일일 최대 요금 (원, 서울만) | 30900.0 |
| `period_fee` | number | 기간 요금 (원, 서울만) | 176000 |
| `payment_method` | string | 결제 방법 (경기만) | "카드결제" |

### 기타 필드

| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `update_time` | string | 업데이트 시간 (서울만) | "2025-12-10 10:24:30" |
| `notice` | string | 안내 메시지 (기타 지역만) | "해당 지역은 기본 주차장 정보만..." |

---

## 응답 예시

### 성공 응답

```json
{
  "parkings": [
    {
      "name": "서울시청 주차장",
      "address": "서울 중구 세종대로 110",
      "total_spots": 1260,
      "available_spots": 507,
      "fee": "교통,지하철 > 지하철역 > 주차장",
      "distance": 62,
      "operating_info": {
        "operating_type": "시간제 운영",
        "weekday_start": "0000",
        "weekday_end": "2400",
        "weekend_start": "0000",
        "weekend_end": "2400",
        "holiday_start": "0000",
        "holiday_end": "2400"
      },
      "fee_info": {
        "is_paid": "유료",
        "basic_fee": 430.0,
        "basic_hours": 5.0,
        "additional_fee": 430.0,
        "additional_hours": 5.0,
        "daily_max_fee": 30900.0
      },
      "update_time": "2025-12-10 10:24:30"
    }
  ],
  "count": 1
}
```

### 에러 응답

```json
{
  "error": "주차장 정보를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
  "parkings": []
}
```

---

## 지역별 제공 정보 요약

| 정보 | 서울 | 경기 | 기타 |
|------|------|------|------|
| 기본 정보 (이름, 주소) | ✅ | ✅ | ✅ |
| 총 주차 대수 | ✅ | ✅ | ❌ |
| 실시간 주차 가능 대수 | ✅ | ❌ | ❌ |
| 운영 시간 | ✅ | ✅ | ❌ |
| 요금 정보 | ✅ | ✅ | ❌ |
| 업데이트 시간 | ✅ | ❌ | ❌ |
| 안내 메시지 | ❌ | ❌ | ✅ |

