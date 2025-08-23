pipeline {
  agent any

  // Ejecutar automáticamente cada hora
  triggers {
    cron('H * * * *')
  }

  options {
    timestamps()
    ansiColor('xterm')
    buildDiscarder(logRotator(numToKeepStr: '20'))
    timeout(time: 20, unit: 'MINUTES')
  }

  environment {
    PYTHON       = 'python3'
    VENV_DIR     = '.venv'
    PIP_CACHE    = '.pip-cache'
    CI           = 'true'
    JENKINS_RUN  = 'true'
  }

  stages {

    stage('Checkout') {
      steps {
        checkout([$class: 'GitSCM',
          branches: [[name: "*/main"]],
          userRemoteConfigs: [[url: 'https://github.com/nicolasgemio/Depto-Alquiler-Scrapping.git', credentialsId: 'github-token']]
        ])
        sh 'echo "Archivos en el workspace:" && ls -la'
      }
    }

    stage('Preparar entorno (venv + deps)') {
      steps {
        sh '''
          set -e
          if [ ! -d "${VENV_DIR}" ]; then
            ${PYTHON} -m venv "${VENV_DIR}"
          fi
          . "${VENV_DIR}/bin/activate"
          python --version
          mkdir -p "${PIP_CACHE}"
          python -m pip install --upgrade pip wheel
          if [ -f requirements.txt ]; then
            PIP_NO_INPUT=1 python -m pip install --cache-dir "${PIP_CACHE}" -r requirements.txt
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
            for v in BASE_URI MERCADOLIBRE_URL ARGENPROP_URL SMTP_SERVER SMTP_PORT EMAIL_USUARIO DESTINATARIO DB_SERVER DB_NAME DB_USER DB_PASSWORD; do
              if [ -n "$(printenv "$v")" ]; then
                echo "✅ $v = set"
              else
                echo "❌ $v = (empty)"
              fi
            done
          '''
        }
      }
    }

    stage('Limpiar logs/data') {
      steps {
        sh '''
          set -e
          mkdir -p logs data
          rm -f logs/*.log
        '''
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
            . "${VENV_DIR}/bin/activate"
            export PYTHONUTF8=1
            export LANG=C.UTF-8
            export LC_ALL=C.UTF-8
            python main.py > "logs/run_$(date +%F_%H%M%S).log" 2>&1 || true
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