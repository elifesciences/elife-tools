elifeLibrary {
    stage 'Checkout', {
        checkout scm
    }

    stage 'Project tests', {
        elifeLocalTests "./project_tests.sh"
    }

    elifeMainlineOnly {
        stage 'Downstream', {
            build job: 'dependencies-bot-lax-adaptor-update-elife-tools', wait: false
        }
    }
}
