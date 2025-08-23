pipeline {
  agent any

  options {
    timestamps()
    ansiColor('xterm')
    buildDiscarder(logRotator(numToKeepStr: '20'))
    timeout(time: 20, unit: 'MINUTES')
  }

  environment {
    PYTHON   = 'python3'
    VENV_DIR = '.venv'
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
        sh 'echo "Archivos en el workspace:" && ls -la'
      }
    }

    stage('Preparar entorno (venv + deps)') {
      steps {
        sh '''
          set -e
          if [ ! -d "${VENV_DIR}" ]; then
            ${PYTHON} -m venv ${VENV_DIR}
          fi
          . ${VENV_DIR}/bin/activate
          python --version
          pip install --upgrade pip wheel
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
          else
            echo "No hay requirements.txt; continuo..."
          fi
        '''
      }
    }

    stage('Sanity env') {
      steps {
        withCredentials([
          string(credentialsId: 'BASE_URI',          variable: 'BASE_URI'),
          string(credentialsId: 'MERCADOLIBRE_URL',  variable: 'MERCADOLIBRE_URL'),
          string(credentialsId: 'ARGENPROP_URL',     variable: 'ARGENPROP_URL'),
          string(credentialsId: 'SMTP_SERVER',       variable: 'SMTP_SERVER'),
          string(credentialsId: 'SMTP_PORT',         variable: 'SMTP_PORT'),
          string(credentialsId: 'EMAIL_USUARIO',     variable: 'EMAIL_USUARIO'),
          string(credentialsId: 'EMAIL_PASSWORD',    variable: 'EMAIL_PASSWORD'),
          string(credentialsId: 'DESTINATARIO',      variable: 'DESTINATARIO'),
          string(credentialsId: 'DB_SERVER',         variable: 'DB_SERVER'),
          string(credentialsId: 'DB_NAME',           variable: 'DB_NAME'),
          string(credentialsId: 'DB_USER',           variable: 'DB_USER'),
          string(credentialsId: 'DB_PASSWORD',       variable: 'DB_PASSWORD')
        ]) {
          sh '''
            set -e
            check_var () { v="$1"; val="${!v:-}"; [ -n "$val" ] && echo "✅ $v = set" || echo "❌ $v = (empty)"; }
            for v in MERCADOLIBRE_URL ARGENPROP_URL BASE_URI SMTP_SERVER SMTP_PORT EMAIL_USUARIO DESTINATARIO DB_SERVER DB_NAME DB_USER DB_PASSWORD; do
              check_var "$v"
            done

            missing=()
            for v in BASE_URI DB_SERVER DB_NAME DB_USER DB_PASSWORD; do
              [ -n "${!v:-}" ] || missing+=("$v")
            done
            if [ ${#missing[@]} -gt 0 ]; then
              echo "FALTAN variables críticas: ${missing[*]}"
              exit 1
            fi
          '''
        }
      }
    }

    stage('Ejecutar scraper') {
      steps {
        withCredentials([
          string(credentialsId: 'BASE_URI',          variable: 'BASE_URI'),
          string(credentialsId: 'MERCADOLIBRE_URL',  variable: 'MERCADOLIBRE_URL'),
          string(credentialsId: 'ARGENPROP_URL',     variable: 'ARGENPROP_URL'),
          string(credentialsId: 'SMTP_SERVER',       variable: 'SMTP_SERVER'),
          string(credentialsId: 'SMTP_PORT',         variable: 'SMTP_PORT'),
          string(credentialsId: 'EMAIL_USUARIO',     variable: 'EMAIL_USUARIO'),
          string(credentialsId: 'EMAIL_PASSWORD',    variable: 'EMAIL_PASSWORD'),
          string(credentialsId: 'DESTINATARIO',      variable: 'DESTINATARIO'),
          string(credentialsId: 'DB_SERVER',         variable: 'DB_SERVER'),
          string(credentialsId: 'DB_NAME',           variable: 'DB_NAME'),
          string(credentialsId: 'DB_USER',           variable: 'DB_USER'),
          string(credentialsId: 'DB_PASSWORD',       variable: 'DB_PASSWORD')
        ]) {
          sh '''
            set -e
            . ${VENV_DIR}/bin/activate
            mkdir -p logs data
            python main.py > logs/run_$(date +%F_%H%M%S).log 2>&1 || true
          '''
        }
      }
    }

    stage('Archivar artefactos') {
      steps {
        archiveArtifacts artifacts: 'logs/**,data/**', allowEmptyArchive: true
      }
    }
  }

  post {
    success { echo '✅ OK' }
    failure { echo '❌ Falló el build. Revisá los logs.' }
  }
}
