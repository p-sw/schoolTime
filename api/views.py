from django.http.response import JsonResponse
import requests
from datetime import datetime, timezone, timedelta
from os import environ

API_KEY = environ.get("NEIS_API_KEY", None)
if not API_KEY:
    raise Exception("NEIS API KEY NOT SET. PLEASE SET KEY WITH ENVIRONMENT VARIABLE NAMED NEIS_API_KEY.")
TIMEZONE = timezone(offset=timedelta(hours=9))

bad_request = JsonResponse({
    "error": True,
    "reason": "Bad Request"
}, status=400)


async def out_response_maker(api_response, result_key):
    if api_response.status_code != 200:
        return JsonResponse({
            "error": True,
            "reason": api_response.reason
        }, status=500)

    data = api_response.json()
    if "RESULT" in data.keys():
        error_code = data['RESULT']['CODE']
        error_reason = data['RESULT']['MESSAGE']
        if error_code == "INFO-200":
            return JsonResponse({
                "error": False,
                "data": []
            })
        return JsonResponse({
            "error": True,
            "reason": f"{error_code} | {error_reason}"
        }, status=500)
    return JsonResponse({
        "error": False,
        "data": data[result_key][1]["row"]
    })


async def school_search(req):
    name = req.GET.get("name", "")
    api_call = requests.get(f"https://open.neis.go.kr/hub/schoolInfo?Type=json&KEY={API_KEY}&SCHUL_NM={name}")
    return await out_response_maker(api_call, "schoolInfo")


async def school_get_time(req):
    if not (school_grade := req.GET.get("sg", None)):
        return bad_request
    if not (edu_govern_code := req.GET.get("egc", None)):
        return bad_request
    if not (school_code := req.GET.get("sc", None)):
        return bad_request

    now = datetime.now(tz=TIMEZONE)

    from_time = req.GET.get("ft", (now - timedelta(days=now.weekday())).strftime("%Y%m%d"))
    to_time = req.GET.get("tt", (now + timedelta(days=(4 - now.weekday()))).strftime("%Y%m%d"))
    grade = req.GET.get("g", "1")
    class_ = req.GET.get("c", "1")

    api_call = requests.get(
        f"https://open.neis.go.kr/hub/{school_grade}Timetable"
        f"?Type=json"
        f"&KEY={API_KEY}"
        f"&ATPT_OFCDC_SC_CODE={edu_govern_code}"
        f"&SD_SCHUL_CODE={school_code}"
        f"&GRADE={grade}"
        f"&CLASS_NM={class_}"
        f"&TI_FROM_YMD={from_time}"
        f"&TI_TO_YMD={to_time}"
    )
    return await out_response_maker(api_call, f"{school_grade}Timetable")


async def school_get_meal(req):
    if not (edu_govern_code := req.GET.get("egc", None)):
        return bad_request
    if not (school_code := req.GET.get("sc", None)):
        return bad_request

    meal_date = req.GET.get("date", datetime.now(tz=TIMEZONE).strftime("%Y%m%d"))

    api_call = requests.get(
        f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={API_KEY}&Type=json"
        f"&ATPT_OFCDC_SC_CODE={edu_govern_code}"
        f"&SD_SCHUL_CODE={school_code}"
        f"&MLSV_YMD={meal_date}"
    )
    return await out_response_maker(api_call, "mealServiceDietInfo")
