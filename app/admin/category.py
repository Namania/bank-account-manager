from django.contrib import admin

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["label"]
    fields = ["label"]