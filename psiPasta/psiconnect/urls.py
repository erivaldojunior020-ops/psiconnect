from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('', views.login_paciente, name='home'),

    path('cadastro_paciente/', views.cadastro_paciente, name='cadastro_paciente'),
    path('login_paciente/', views.login_paciente, name='login_paciente'),
    path('inicio_paciente/', views.inicio_paciente, name="inicio_paciente"),
    path('lista_psicologos/', views.lista_psicologos, name='lista_psicologos'),
    path('agendamento_paciente/<int:psicologo_id>/', views.agendamento_paciente, name='agendamento_paciente'),
    path('sessoes_paciente/', views.sessoes_paciente, name='sessoes_paciente'),
    path('cancelar_sessao_ajax/<int:sessao_id>/', views.cancelar_sessao_ajax, name='cancelar_sessao_ajax'),
    path('sobre_paciente/', views.sobre_paciente, name='sobre_paciente'),
    path('servicos_paciente/', views.serviços_paciente, name='servicos_paciente'),
    path('suporte_paciente/', views.suporte_paciente, name='suporte_paciente'),

    path('login_professor/', views.login_professor, name='login_professor'),
    path('cadastrar_aluno/', views.cadastrar_aluno, name='cadastrar_aluno'),

    path("chat/<int:consulta_id>/", views.chat, name="chat"),

    path('login_psicologo/', views.login_psicologo, name='login_psicologo'),
    path('inicio_psicologo/', views.inicio_psicologo, name='inicio_psicologo'),
    path('perfil_psicologo/', views.perfil_psicologo, name='perfil_psicologo'),
    path("cadastrar_horario/", views.cadastrar_horario, name="cadastrar_horario"),
    path('consultas_psicologo/', views.consultas_psicologo, name='consultas_psicologo'),
    path("consulta/<int:id>/confirmar/", views.confirmar_consulta, name="confirmar_consulta"),
    path("consulta/<int:id>/cancelar/", views.cancelar_consulta, name="cancelar_consulta"),
    path("consulta/<int:id>/pendente/", views.pendente_consulta, name="pendente_consulta"),
    

]
