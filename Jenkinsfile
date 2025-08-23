pipeline {
  agent any

  options {
    timestamps()
    ansiColor('xterm')
    buildDiscarder(logRotator(numToKeepStr: '20'))
    timeout(time: 20, unit: 'MINUTES')
  }

  environment {
    PYTHON = 'python3'
    VENV_DIR = '.venv'
    MERCADOLIBRE_URL=credentials('MERCADOLIBRE_URL')
    ARGENPROP_URL=credentials('ARGENPROP_URL')
    SMTP_SERVER=credentials('SMTP_SERVER')
    SMTP_PORT=credentials('SMTP_PORT')
    EMAIL_USUARIO=credentials('EMAIL_USUARIO')
    EMAIL_PASSWORD=credentials('EMAIL_PASSWORD')
    DESTINATARIO=credentials('DESTINATARIO')
    BASE_URI=credentials('BASE_URI')
    DB_USER=credentials('DB_USER')
    DB_PASSWORD=credentials('DB_PASSWORD')
    DB_SERVER=credentials('DB_SERVER')
    DB_NAME=credentials('DB_NAME')
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
