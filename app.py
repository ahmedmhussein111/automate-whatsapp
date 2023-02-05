from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

# Replace YOUR_URL with your mongodb url
cluster = MongoClient("mongodb+srv://admin:admin@cluster0.bihtyrb.mongodb.net/?retryWrites=true&w=majority")
db = cluster["bakery"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")[:-2]
    res = MessagingResponse()
    user = users.find_one({"number": number})
    if user["status"] == "main" or user["status"] == "UnivApproval" or user["status"] == "StudentInquery" or user["status"] == "GraduatedInquery" or user["status"] == "OtherInquery":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)

        if option == 0:
            res.message("القائمة الرئيسية *لعمادة القبول والتسجيل*"
                        "\n"
                        " يرجي إدخال رقم الخدمة بناء علي نوع الإستفسار الخاص بكم:" "\n \n"
                        "1️⃣ للإستفسار عن القبول بالجامعة" "\n"
                        "2️⃣ لإستفسارات طلاب الجامعة" "\n"
                        "3️⃣ لإستفسارات الخريجين" "\n"
                        "4️⃣ للإستفسارات الأخري" "\n")

        elif option == 1:
            res.message("*الإستفسار عن القبول بالجامعة*\n"
                        "1️⃣ للقبول بمرحلة البكالوريوس لحملة شهادة الثانوية العامة:\n"
                        "2️⃣ للقبول ببرامج الماجستير والدبلوم العالي:\n"
                        "3️⃣ للقبول ببرنامج بكالوريوس الطب (المسار الثاني) لحملة درجة البكالوريوس في التخصصات المطلوبة:\n"
                        "0️⃣ للرجوع للقائمة السابقة:")
            users.update_one(
                {"number": number}, {"$set": {"status": "UnivApproval"}})
        elif option == 2:
            users.update_one(
                {"number": number}, {"$set": {"status": "StudentInquery"}})
            res.message("*استفسارات طلاب الجامعة*\n"
                        "1️⃣ للإستعلام عن طلب تغيير الحالة الأكاديمية ( الإنسحاب من الجامعة) او الإعتذار عن إكمال الدراسة:\n"
                        "2️⃣ الإستعلام عن المواعيد المحددة لتقديم طلب:\n"
                        "3️⃣ الإستعلام عن حالة الطلب في نظام المعلومات الطلابي:\n"
                        "4️⃣ الإستعلام عن المكافآت:\n"
                        "0️⃣ للرجوع للقائمة السابقة:")
        elif option == 3:
            users.update_one(
                {"number": number}, {"$set": {"status": "GraduatedInquery"}})
            res.message("*استفسارات الخريجين*\n"
                        "1️⃣ لطلب الشهادة المؤقتة:\n"
                        "2️⃣ للإستعلام عن إستلام الوثائق:\n"
                        "3️⃣ لطلب سجل أكاديمي:\n"
                        "4️⃣ للتحقق من وثائق الخريجين:\n"
                        "0️⃣ للرجوع للقائمة السابقة:")
        elif option == 4:
            users.update_one(
                {"number": number}, {"$set": {"status": "OtherInquery"}})
            res.message("*الإستفسارات الأخري*\n"
                         "\n"
                        "الأسئلة الشائعة"
                        "\n"
                        "https://ksau-hs.edu.sa/Arabic/Admission/Pages/FAQs.aspx"
                        "\n"
                        "دليل المستخدم"
                        "\n"
                        "https://ksau-hs.edu.sa/Arabic/Admission/Pages/AdmissionGuide.aspx"
                        )

        else:
            res.message("Please enter a valid response")
    else:
        res.message(" \n اهلا وسهلا بكم في *عمادة القبول والتسجيل*"
                    "\n"
                    " يرجي إدخال رقم الخدمة بناء علي نوع الإستفسار الخاص بكم:" "\n \n"
                    "1️⃣ للإستفسار عن القبول بالجامعة" "\n"
                    "2️⃣ لإستفسارات طلاب الجامعة" "\n"
                    "3️⃣ لإستفسارات الخريجين" "\n"
                    "4️⃣ للإستفسارات الأخري" "\n")

        res.media("https://ksau-hs.edu.sa/_catalogs/masterpage/KSAUPortal/image/KSAU-HS%20logos-02.svg")
        users.insert_one({"number": number, "status": "new", "messages": []})
    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(res)


if __name__ == "__main__":
    app.run()
