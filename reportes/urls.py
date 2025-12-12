from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('citas/', views.reporte_citas, name='reporte_citas'),
    path('doctores/', views.reporte_doctores, name='reporte_doctores'),
    path('pacientes/', views.reporte_pacientes, name='reporte_pacientes'),
    path('exportar/excel/citas/', views.exportar_excel_citas, name='exportar_excel_citas'),
    path('exportar/pdf/citas/', views.exportar_pdf_citas, name='exportar_pdf_citas'),
]
