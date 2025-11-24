# 📘 Portfólio Completo — **Psiconnect**

Plataforma moderna de atendimento psicológico online, desenvolvida para psicólogos e pacientes, com foco em **agilidade**, **segurança**, **usabilidade** e **experiência profissional**.

---

## 🚀 **Visão Geral do Projeto**

A **Psiconnect** é uma plataforma web desenvolvida para facilitar o agendamento, gerenciamento e realização de atendimentos psicológicos online. O objetivo é aproximar profissionais e pacientes por meio de uma ferramenta simples, intuitiva e funcional — totalmente responsiva e pensada para uso real.

O sistema conta com recursos completos para psicólogos, pacientes e administração, contemplando desde cadastro e login até consultas em tempo real.

---

## 🧩 **Funcionalidades Principais**

### 👤 **Área do Psicólogo**

* Cadastro e login seguro
* Dashboard com visão geral de atendimentos
* Visualização de consultas marcadas
* Agenda semanal e diária
* Edição de perfil (bio, imagem, informações profissionais)
* Upload e exibição de imagem de perfil
* Chat em tempo real com os pacientes
* Gerenciamento de horários disponíveis

### 🧑‍🤝‍🧑 **Área do Paciente**

* Cadastro e login
* Seleção de psicólogos
* Agendamento de consultas
* Histórico de sessões
* Chat com psicólogo
* Edição de informações pessoais

### 💬 **Chat em Tempo Real**

* WebSocket integrado
* Envio de mensagens instantâneas
* Marcação de horário em cada mensagem
* Interface moderna com "bolhas" de chat

### 📅 **Agendamento e Sessões**

* Marcação de consulta com confirmação automática
* Exibição clara de datas e horários
* Painel para psicólogos com consultas marcadas

### 🎨 **Interface (Frontend)**

* Design moderno baseado em estilos do Figma
* Temas com gradiente azul-turquesa característico da marca Psiconnect
* Templates HTML responsivos e limpos
* Versões adaptadas para desktop e mobile

---

## 🏗️ **Arquitetura do Projeto**

### **Frontend (HTML, CSS, JS)**

* Templates modernos criados manualmente
* Uso de gradientes lineares e layouts responsivos
* Integrações com WebSockets
* Chamadas AJAX/Fetch para a API
* Interface intuitiva com foco profissional

### **Backend (Django)**

* Sistema de autenticação completo (login/logout)
* Modelos para Psicólogo, Paciente, Consulta e Chat
* Views e rotas organizadas
* Upload de imagens com ImageField
* Integração com WebSockets (Django Channels)
* Renderização dinâmica de templates

### **Banco de Dados**

* MYSQL 
* Tabelas principais:

  * `User`
  * `Paciente`
  * `Psicologo`
  * `Consulta`
  * `Mensagem`

### **WebSockets (Chat)**

* Canal de comunicação instantânea paciente ↔ psicólogo em formação
* JsonResponse personalizado
* Estrutura escalável para múltiplas conversas simultâneas

---

## 🧪 **Funcionalidades Técnicas Implementadas**

### 🔐 **Autenticação**

* Sistema completo com Django Auth
* Perfis separados para psicólogo e paciente
* Redirecionamento inteligente

### 🖼️ **Upload de Imagens (perfil)**

* Implementação correta com MEDIA_URL e MEDIA_ROOT
* Visualização da imagem no template

### 📡 **Chat em Tempo Real**

* Django Channels
* Sistema de salas individuais por consulta
* Mensagens com horário e formatação

### 🛠️ **Templates Ajustados**

* Correções de erros
* Ajustes de responsividade
* Adaptação de modelos enviados pelo usuário
* Ajustes visuais e estruturais

---

## 🎯 **Objetivo da Plataforma**

A Psiconnect surgiu com o objetivo de:

* Facilitar o acesso a atendimento psicológico 
* Modernizar a rotina profissional dos psicólogos em formação 
* Oferecer uma plataforma intuitiva e rápida
* Permitir consultas, conversas e agendamentos em um só lugar
* Centralizar todo o processo terapêutico

E o mais importante: **continuar evoluindo**, com novas funcionalidades como:

* Chamadas de vídeo integradas
* Notificações em tempo real
* Melhorias de UX
* Área administrativa completa

---

## 💡 **Diferenciais do Projeto**

* Código limpo e organizado
* Uso de WebSockets
* Templates modernos e autorais
* Arquitetura escalável
* Sistema completo para psicólogos em formação  e pacientes

---

## 🛠️ **Como rodar o projeto**

### **1. Clonar o repositório**

```
git clone https://github.com/seu-usuario/psiconnect.git
cd psiconnect
```

### **2. Criar ambiente virtual**

```
python -m venv venv
venv/Scripts/activate
```

### **3. Instalar dependências**

```
pip install -r requirements.txt
```

### **4. Aplicar migrações**

```
python manage.py migrate
```

### **5. Rodar o servidor**

```
python manage.py runserver
```

Pronto! O sistema estará disponível em:

```
http://localhost:8000
```

## 👨‍💻 **Tecnologias Utilizadas**

* **Python 3**
* **Django**
* **Django Channels**
* **HTML / CSS / JavaScript**
* **WebSockets**
* **SQLite / MySQL (opcional)**
* **Pillow** para imagens

---

## 📌 **Sobre o Desenvolvimento**

Todo o projeto foi construído com foco em:

* Aprendizado
* Melhores práticas
* Expansibilidade
* Uso real para psicólogos

A Psiconnect continuará evoluindo — novas ideias já estão planejadas, como chamadas por vídeo, notificações e ferramentas avançadas.

