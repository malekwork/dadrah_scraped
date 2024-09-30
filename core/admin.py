from django.contrib import admin
from .models import Lawyer, Question, Answer

class LawyerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city')  # فیلدهایی که در لیست نمایش داده می‌شوند
    search_fields = ('name', 'city')  # قابلیت جستجو در فیلدهای name و city

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1  # تعداد فیلدهای اضافی برای اضافه کردن پاسخ‌های جدید

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date')  # فیلدهایی که در لیست نمایش داده می‌شوند
    search_fields = ('title', 'date')  # قابلیت جستجو در فیلدهای title و date
    inlines = [AnswerInline]  # اضافه کردن پاسخ‌ها به صورت درون خطی در جزئیات سوال

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'lawyer', 'text')  # فیلدهایی که در لیست نمایش داده می‌شوند
    search_fields = ('question__title', 'lawyer__name', 'text')  # جستجو بر اساس عنوان سوال، نام وکیل و متن پاسخ

# ثبت مدل‌ها در پنل ادمین
admin.site.register(Lawyer, LawyerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
