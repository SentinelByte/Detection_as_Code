# Detection as Code (ELK Stack)

Welcome to the **Detection as Code Pipeline** repository! This project aims to streamline and enhance threat detection through a robust, scalable pipeline built on the principles of "detection as code." This repository provides a comprehensive solution for creating, testing, and deploying detection rules in a systematic and automated manner. ***This Repo focus with ELK stack !!!***.


## 📋 Overview

***This Repo focus with ELK stack !!!***.
The Detection as Code Pipeline is designed to bridge the gap between detection engineering and development practices. It enables security teams to define, test, and manage detection rules as code, ensuring that these rules are both effective and maintainable. This approach brings the benefits of version control, automated testing, and continuous integration to the realm of security detection.


## 🚀 Features

- **Detection as Code**: Define and manage your detection rules in code, making them easily versioned and reviewed.
- **Automated Testing**: Run automated tests on your detection rules to ensure their accuracy and effectiveness before deployment.
- **Continuous Integration**: Integrate with CI/CD pipelines to automate the deployment and updating of detection rules.
- **Scalability**: Designed to scale with your organization's needs, handling complex rule sets and large datasets efficiently.
- **Documentation and Examples**: Comprehensive documentation and example configurations to get you started quickly.


## 🛠️ Getting Started

### Prerequisites

Before you start, ensure you have the following installed:
- [Python](https://www.python.org/) (version 3.8 or higher)
- [Docker](https://www.docker.com/) (for containerized environments)
- [Requests](https://pypi.org/project/requests/)
- [Elastic_Cloud](https://www.elastic.co/guide/en/security/current/security-apis.html)


### Installation and Usage

1. ***Clone the Repository***

   ```
   git clone https://github.com/SentinelByte/Detection_as_Code.git
   cd detection-as-code
   ```

2. ***Store the create_json.py for custom runs***

   Create a dedicated VM (Virtual Machine) on your prefered cloud provider (GCP/AWS/Azure/etc.) and store the create_json.py code.
   
   Altrernatively, you can use a local machine (Note! just make sure you have a proper allowed connection to the ELK SaaS and API Endpoints).

   Upon detection rule creation, you will trigger manually this code and it will take you through the process of a JSON file creation, that will be used later for the detection rule creation.

3. ***Set up a push job to your CICD tool***

   To run the code and create the detection rule, push ths json file to your CICD tool (Jenkins/ GitLab CI/CD/ Circle CI/ etc).
   
   The job should fetch a JSON file created from the crate_json.py code.
   
   3.1. Set up a cron job/ bash/ or other method to push the json file created from step 2 to your Github account.

   If you don't want to use a github account, fill free to use any other solution for that.

   You can even choose to push the json file directly to a cicd tool you choose (Jenkins/ GitLab CI/CD/ Circle CI/ etc.)

   3.2. setup permissions - chmod +x ~/push_and_archive.sh

   3.3 Open crontab and create the cron job:
   
   ```
   crontab -e
   0 * * * * /bin/bash ~/push_to_github.sh
   ```
   
   ** Note! You can adjust the cron job interval to your needs.
   
5. ***Set Up CI Environment***
   
   Use Github Actions/ Juenkins/ etc.
   If needed, create a virtual environment and install dependencies:

   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

7. ***Configure the Pipeline***

   Update the configuration files located in the `config` directory.
   you will need to run the following:
   - create_rule.py
   - check_query_main.py
  
     ** Make sure you upload the following also:
      - validate_qury.py
      - check_query.py

9. ***Run the Pipeline***

   Start the pipeline using Docker:

   ```
   docker-compose up
   ```

   Or run locally:

   ```
   python3 craft_json.py
   python3 create_rule.py
   python3 check_query_main.py
   ```


## 🧪 Testing

You can run this code locally and see if everything works.
Make sure you have connection between your local machine to the Elastic endpint.
To ensure your detection rules are functioning as expected, run the following one by one:
1. craft_json.py
2. create_rile.py
3. check_query_main.py


## 📝 Documentation

For more detailed information on how to use and customize the Detection as Code refere to the comments within the code.


## 🤝 Acknowledgements

Provide ideas and inspiration for this project: https://medium.com/threatpunter/from-soup-to-nuts-building-a-detection-as-code-pipeline-28945015fc38

© SentinelByte | dancohvax

Happy detecting! 🚀🔍
