# ✈️ **Azure Data Engineering End-to-End Project: Aviation**

---

📑 **Table of Contents**

- 🔵 [Project Overview](#project-overview)
- 🔵 [Expected Outputs](#expected-outputs)
- 🔵 [Data Sources and Transformation](#data-sources-and-transformation)
- 🔵 [Data Set Selection](#data-set-selection)
- 🔵 [Technology Choices](#technology-choices)
- 🔵 [Data Model](#data-model)
- 🔵 [Implementation Steps](#implementation-steps)
- 🔵 [CI/CD and Automation](#cicd-and-automation)
- 🔵 [Alternatives Considered](#alternatives-considered)
- 🔵 [Future Enhancements](#future-enhancements)

---

## 📝 **Project Overview**

This end-to-end project demonstrates a comprehensive data engineering solution on the Azure platform, designed to process and analyze aviation-related data. Using data from multiple sources, the project involves data ingestion, transformation, and loading into a structured data model to facilitate analytical queries, reporting, and visualization through Power BI. The project employs scalable and automated Azure services to ensure reliability, efficiency, and ease of management.

---

## 🎯 **Expected Outputs**

By the end of this project, we expect to produce:

- 📂 **Layered Data Storage**: Organized data in Azure Data Lake Storage (ADLS) across raw, cleansed, and mart layers.
- 🔍 **Data Quality Checks**: Automated data validation using Databricks, ensuring integrity in the mart layer.
- 🏢 **SQL Data Warehouse Views**: Optimized views for fast and efficient querying, specifically set up for Power BI reporting.
- 📊 **Power BI Dashboard**: A dynamic visualization of insights into airline operations, cancellations, and other metrics.
- 📧 **Automated Notifications**: Email alerts using Azure Logic Apps, sending reports to stakeholders listed in an Excel file.

---

## 📈 **Data Sources and Transformation**

This project incorporates six primary data sources, processed as follows:

1. **Plane Data**: Retrieved as a PDF from client blob storage, converted to CSV, and loaded into the ADLS raw storage layer.
2. **Flight Data**: CSV files for years 2005 to 2008 were ingested from the client’s data lake into the ADLS raw layer.
3. **Airport Data**: Loaded from the client’s data lake storage into ADLS.
4. **Airlines Data**: Pulled from the Airlabs API and stored in the ADLS raw storage layer.
5. **Cancellation Data**: Extracted from the client’s SQL Database (SQL DB) into ADLS.
6. **Unique Carriers Data**: Retrieved from the client’s SQL Database (SQL DB) and stored in ADLS.

These data sources are cleansed and standardized using Databricks with both autoloader and batch processing. After transformation, the data is organized into dimension and fact tables within a mart layer. Data quality checks are applied in Databricks to ensure accuracy and consistency.

---

## 📂 **Data Set Selection**

Each dataset was chosen to support detailed analysis:

- **Plane & Flight Data**: For tracking operational performance over time.
- **Airport & Airlines Data**: To enrich flight data with information about carriers and locations.
- **Cancellation & Unique Carriers Data**: Enables analysis of flight disruptions and airline metrics.

### Justification:
These datasets provide a comprehensive view of aviation operations, facilitating detailed and valuable insights.

---

## 💻 **Technology Choices**

The project uses a suite of Azure tools, each chosen for its unique capabilities:

- **Azure Data Lake Storage (ADLS)** 🗄️: For storing raw, cleansed, and mart data with hierarchical organization.
- **Azure Data Factory (ADF)** 🛠️: To manage ETL processes and ensure data pipeline efficiency, with filter activity for selective retries.
- **Databricks** 🔍: For data cleansing and transformation, using autoloader and batch processing along with data quality checks.
- **Azure SQL Database (SQL DB)** 🗄️: Acts as a staging area for Cancellation and Unique Carriers data, allowing for more flexible data management and integration.
- **Azure SQL Data Warehouse (SQL DW)** 🏛️: For hosting the final data model with views optimized for reporting and analysis, specifically designed for large-scale queries.
- **Azure Logic Apps** 🔔: To automate email notifications, sending regular updates to listed contacts.
- **Azure Automation Account** ⚙️: To manage start and stop operations for the SQL Data Warehouse, optimizing cost.
- **CI/CD Pipelines (Azure DevOps & GitHub Actions)** 🚀: For smooth integration and deployment, with automated triggers, global parameters, and manual file support.

### Justification:
This stack was selected for its integration capabilities, scalability, and automation features, making it ideal for enterprise-scale data projects.

---

## 🗂️ **Data Model**

The data model follows a star schema design with:

- **Fact Table**: Core Flight data, detailing each flight with information on dates, cancellations, and other metrics.
- **Dimension Tables**: Separate tables for Plane, Airport, Airlines, Cancellation, and Unique Carriers, enriching the context around Flight data.
- **📅 Date Dimension Table**: Added at the Power BI stage, this table allows time-based filtering and trend analysis by day, month, quarter, and year.

### Rationale:
This star schema, enhanced by the Date Dimension, improves performance for analytical queries and is optimized for Power BI’s reporting requirements.

---

## 🚀 **Implementation Steps**

1. **Data Ingestion** 🔄: Moved raw data from client sources (blob storage, data lake, SQL database) into our ADLS raw storage using ADF.
2. **Data Transformation** ✨: Cleaned and standardized the data with Databricks (autoloader and batch processing) before loading to the cleansed layer in ADLS.
3. **Data Modeling** 🧩: Organized the data into a star schema (fact and dimension tables) in the mart layer, with quality checks in Databricks.
4. **Data Loading** 📥: Loaded mart data into the SQL Data Warehouse to support analytical reporting, creating optimized views.
5. **Dashboard Creation** 📊: Built a Power BI dashboard for visualization, including a Date Dimension table to support detailed temporal analysis.
6. **Email Automation** 📧: Set up Azure Logic App to send updates to contacts listed in an Excel file.
7. **Resource Automation** 💼: Used Azure Automation Account to manage SQL Data Warehouse operations, reducing costs by automating start/stop schedules.

---

## 🔄 **CI/CD and Automation**

The project’s CI/CD pipeline automates deployment and updates across various Azure services, providing seamless integration and efficient management. Key elements include:

1. **GitHub Actions for Lookup Files and Data Factory Deployment** 🔎:
   - **Manual File Addition**: Used GitHub Actions to add manual files required for the lookup activity in ADF, ensuring files are up-to-date and accessible in the ADF pipeline.
   - **ADF Deployment**: Deployed ADF pipelines with GitHub Actions, including triggers and global parameters to manage and streamline pipeline execution.

2. **Databricks Notebook Deployment with GitHub Actions** 📑:
   - GitHub Actions were configured to automatically deploy Databricks notebooks, ensuring that the latest code and transformations are consistently applied in the data pipelines. This deployment includes:
     - **Utility Scripts**: Custom scripts for data quality checks and transformation logic.
     - **Data Transformation Workflows**: Ensures that changes made to cleansing and transformation code are automatically reflected in the production environment.

3. **CI/CD for Azure Data Factory (ADF) Deployment** 🚀:
   - **Global Parameters**: Managed with GitHub Actions to ensure consistent configuration across environments.
   - **Pipeline Triggers**: Configured in ADF for automatic triggering of pipelines, ensuring workflows are only initiated based on defined conditions or schedules.
   - **Failure Handling**: Implemented using the filter activity, allowing selective retries to avoid re-running entire workflows.

4. **Continuous Integration in Azure DevOps** 🧩:
   - Integrated Azure DevOps pipelines to manage testing and deployment for each service update, with GitHub Actions as an alternative deployment path to maintain consistency across tools.

---

## 🤔 **Alternatives Considered**

- **Azure Synapse Analytics for ETL**: Synapse provides an integrated ETL environment, but Databricks was selected for its flexibility with both batch and autoload processes.
- **Blob Storage Instead of ADLS**: ADLS offered better organization and access control, so we opted for it over Blob Storage.
- **Logic Apps for Data Quality Checks**: While Logic Apps could handle validations, Databricks provided a more customizable and scalable solution.

---

## 📈 **Future Enhancements**

To scale and extend the project, consider these options:

1. **Handle Larger Data Volumes 🗄️**: For a 100x data volume increase, partition data in SQL Data Warehouse and explore ADLS tiered storage options.
2. **Integrate Streaming Data 💧**: To support real-time insights, incorporate streaming sources (e.g., live flight data) using Azure Stream Analytics or Databricks.
3. **Scheduled Reporting ⏰**: Automate daily or weekly Power BI report distributions using the Azure Logic App, scheduling delivery at key times (e.g., 9 AM daily).
4. **Expand User Access 🧑‍🤝‍🧑**: Enable concurrent access for multiple teams by configuring user roles and permissions in SQL Data Warehouse, supporting data engineers, scientists, and analysts.

---

## 📸 **Screenshots**

### 🔧 Data Ingestion Process  
![Data Ingestion Process](https://github.com/rileha/Databricks-Certified-Data-Engineer-Professional/blob/main/Screenshots/Screenshot%202025-03-20%20at%2010
