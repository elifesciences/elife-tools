elifeLibrary {
    stage 'Checkout', {
        checkout scm
    }

    elifeVariants(['python2.7', 'python3.5'], { python_versioned ->
        elifeLocalTests "python_versioned=${python_versioned} ./project_tests.sh"
    })

    elifeMainlineOnly {
        stage 'Downstream', {
            build job: 'dependencies-bot-lax-adaptor-update-elife-tools', wait: false
        }
    }
}
