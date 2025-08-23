pipeline {
  agent any

  options {
    timestamps()
    ansiColor('xterm')
    buildDiscarder(logRotator(numToKeepStr: '20'))
    timeout(time: 20, unit: 'MINUTES')
  }

  environment {
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

    stage('Ejecutar scraper') {
      steps {
        sh '''
          set -e
          . ${VENV_DIR}/bin/activate
          mkdir -p logs data
          # Ejecuta tu script principal; ajustá flags si tu main.py acepta argumentos
          python main.py > logs/run_$(date +%F_%H%M%S).log 2>&1 || true
        '''
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
