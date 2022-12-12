# Continuous Integration - Deployment 🌀

Deployment Steps:

- Commit
- Build and Integration Tests
- UAT/Staging/Performance Tests
- Deploy to production

In order to program this steps we can use:

- Trigger by commit
- **Automatic scripts with GitHub Actions**

Continuous Integration: commit + build integration tests <br>
Continuous UAT: Continuous Integration + UAT/Staging/Performance tests<br>
Continuous deployment: Continuous Integration + Continous Delivery + Deployment

DevOps: Developers + Operations Teams 

- DataOps
- MLops (Using GitHub Actions facilitiations for this steps)
    - Model Validation
    - Versioning of the model/dataset
    - Continuous Deployment


# GitHub Actions 🐱

Automation Framework integrated in GitHub

Actions are triggered by:

- Pushes
- Pull Request
- Relases
- ...

Put yaml file in ".git/workflows" to define workflows:

- Event (that trigger the Action)
- Actions (grouped by Jobs)

example yaml file:

        name: Pylint
        on: [push, pull_request] //or on: \n pull_request: branches: -main
        jobs:
            job1: 
                build:
                    runs-on: ubuntu-latest
                    strategy:
                        matrix:
                            python-version: ["3,8", "3.9"]
                    steps:
                    - name: Repo checkout
                    - uses: actions/checkout@v2
                    - run: |
                        cd ./app
                        ls .
            job2:
                needs: [job1, job3] //it means that this job depends on the previous
             

Jobs: are tasks that we want to be performed (limited to 6 hours/job) that can work in parallel or not.

Secrets: allow us to define secret envs that can be used by GitHub and use it with:

        ${{ secrets.SECRET_NAME }}

If we want to save some files of a run we have to use "Artifacts" so files are persisted in gitHub (NB: without artifacts file are saved only during the run then deleted.)

        uses: actions/upload-artifact@v2.3.1
        with: 
            name: artifact_1
            path: ./${{ env.FILE_NAME }}