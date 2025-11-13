from django.urls import path, include
from . import views

urlpatterns = [
    path ('cadastro_paciente/', views.cadastro_paciente, name='cadastro_paciente'),
    path ('login_paciente/', views.login_paciente, name='login_paciente'),
    path ('inicio_paciente/', views.inicio_paciente, name="inicio_paciente"),
    path('lista_psicologos/', views.lista_psicologos, name='lista_psicologos'),
    path('agendamento_paciente/', views.agendamento_paciente, name='agendamento_paciente'),
    path('sessoes_paciente/', views.sessoes_paciente, name='sessoes_paciente'),


    
    path('login_professor/', views.login_professor, name='login_professor'),
    path('cadastrar_aluno/', views.cadastrar_aluno, name='cadastrar_aluno'),


    
    path('login_psicologo/', views.login_psicologo, name='login_psicologo'),
    path('inicio_psicologo/', views.inicio_psicologo, name='inicio_psicologo'),
    path('perfil_psicologo/', views.perfil_psicologo, name='perfil_psicologo'),

]