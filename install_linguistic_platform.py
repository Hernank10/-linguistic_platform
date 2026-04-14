#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

class LinguisticPlatformInstaller:
    def __init__(self):
        self.project_name = "linguistic_platform"
        self.project_path = Path.cwd()
        self.venv_path = self.project_path / "venv"
        
    def print_header(self, text):
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)
    
    def print_success(self, text):
        print(f"✅ {text}")
    
    def print_error(self, text):
        print(f"❌ {text}")
    
    def print_info(self, text):
        print(f"📌 {text}")
    
    def run_command(self, cmd):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    
    def create_virtualenv(self):
        self.print_header("Creando Entorno Virtual")
        if self.venv_path.exists():
            self.print_info("Entorno virtual ya existe")
            return True
        success, _, error = self.run_command(f"python3 -m venv {self.venv_path}")
        if not success:
            self.print_error(f"Error: {error}")
            return False
        self.print_success("Entorno virtual creado")
        return True
    
    def get_pip_path(self):
        return self.venv_path / "bin" / "pip"
    
    def get_python_path(self):
        return self.venv_path / "bin" / "python"
    
    def install_django(self):
        self.print_header("Instalando Django")
        pip_path = self.get_pip_path()
        success, _, error = self.run_command(f"{pip_path} install Django==4.2.7")
        if not success:
            self.print_error(f"Error: {error}")
            return False
        self.print_success("Django instalado")
        return True
    
    def create_project(self):
        self.print_header("Creando Proyecto Django")
        python_path = self.get_python_path()
        
        if not (self.project_path / "manage.py").exists():
            success, _, error = self.run_command(f"{python_path} -m django startproject linguistic_platform .")
            if not success:
                self.print_error(f"Error: {error}")
                return False
        
        for app in ["accounts", "courses", "exercises", "flashcards", "dashboard"]:
            if not (self.project_path / app).exists():
                self.run_command(f"{python_path} manage.py startapp {app}")
        
        self.print_success("Proyecto y apps creadas")
        return True
    
    def fix_settings(self):
        self.print_header("Configurando settings.py")
        settings_path = self.project_path / "linguistic_platform" / "settings.py"
        
        content = '''from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-test-key-2024'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'courses',
    'exercises',
    'flashcards',
    'dashboard',
]
AUTH_USER_MODEL = 'accounts.User'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'linguistic_platform.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
'''
        settings_path.write_text(content)
        self.print_success("settings.py configurado")
        return True
    
    def create_user_model(self):
        self.print_header("Creando modelo de usuario")
        models_path = self.project_path / "accounts" / "models.py"
        
        content = '''from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (('student', 'Estudiante'), ('teacher', 'Profesor'), ('admin', 'Administrador'))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    def __str__(self):
        return self.username
'''
        models_path.write_text(content)
        
        admin_path = self.project_path / "accounts" / "admin.py"
        admin_content = '''from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role',)
    fieldsets = UserAdmin.fieldsets + (('Rol', {'fields': ('role',)}),)
'''
        admin_path.write_text(admin_content)
        
        self.print_success("Modelo de usuario creado")
        return True
    
    def run_migrations(self):
        self.print_header("Ejecutando migraciones")
        python_path = self.get_python_path()
        
        self.run_command(f"{python_path} manage.py makemigrations accounts")
        success, _, error = self.run_command(f"{python_path} manage.py migrate")
        
        if not success:
            self.print_error(f"Error: {error}")
            return False
        
        self.print_success("Migraciones ejecutadas")
        return True
    
    def create_superuser(self):
        self.print_header("Creando superusuario")
        python_path = self.get_python_path()
        
        script = '''
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "linguistic_platform.settings")
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@linguistic.com", "admin123")
    print("Superusuario creado")
'''
        script_path = self.project_path / "create_superuser.py"
        script_path.write_text(script)
        self.run_command(f"{python_path} create_superuser.py")
        script_path.unlink()
        
        self.print_success("Superusuario: admin / admin123")
        return True
    
    def install(self):
        self.print_header("INSTALADOR DE PLATAFORMA LINGUISTICA")
        
        steps = [
            ("Creando entorno virtual", self.create_virtualenv),
            ("Instalando Django", self.install_django),
            ("Creando proyecto", self.create_project),
            ("Configurando settings", self.fix_settings),
            ("Creando modelo User", self.create_user_model),
            ("Ejecutando migraciones", self.run_migrations),
            ("Creando superusuario", self.create_superuser),
        ]
        
        for name, func in steps:
            print(f"\n▶ {name}...")
            if not func():
                self.print_error(f"Fallo en: {name}")
                return False
        
        self.print_header("INSTALACION COMPLETADA")
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║   🎉 Plataforma instalada exitosamente!                     ║
║                                                              ║
║   Para iniciar el servidor:                                 ║
║     cd {self.project_path}                                  ║
║     source venv/bin/activate                                ║
║     python manage.py runserver                              ║
║                                                              ║
║   Acceso admin: http://127.0.0.1:8000/admin/                ║
║   Usuario: admin                                            ║
║   Contraseña: admin123                                      ║
╚══════════════════════════════════════════════════════════════╝
        """)
        return True

if __name__ == "__main__":
    installer = LinguisticPlatformInstaller()
    installer.install()
