
## Contents
- [Prerequisites](#prerequisites)
- [SOP for Initiating Services](#sop-for-initiating-services)
  - [Download Sample Code](#1-download-sample-code)
  - [Install the Azure CLI and Login](#2-install-the-azure-cli-and-login)
  - [Create a resource group](#3-create-a-resource-group)
  - [Create Azure Digital Twin](#4-create-azure-digital-twin)
  - [Set AD for Azure Map](#5-set-ad-for-azure-map)
  - [Upload DWG & manifest.json to Azure Map using Postman](#6-upload-dwg--manifestjson-to-azure-map-using-postman----ref-)
  - [Create & Deploy toADT Function](#7-create--deploy-toadt-function)
  - [Create Azure IoT Hub, Set Event Grid, Create IoT Device](#8-create-azure-iot-hub-set-event-grid-create-iot-device)
  - [Set Event & toTsi Function](#9-set-event--totsi-function)
  - [Create and set TSI Service](#10-create-and-set-tsi-service)
  - [Set Event & toMap Function](#11-set-event--tomap-function)
  - [Set Dashboard and Upload Model](#12-set-dashboard-and-upload-model)
  - [Start Device by running percept_pnp.py](#13-start-device-by-running-percept_pnppy)
  - [Create Twin](#14-create-twin)
  - [Visualize your data in Time Series Insights](#15-visualize-your-data-in-time-series-insights)
  - [View live updates on your dashboard](#16-view-live-updates-on-your-dashboard)
  - [View live updates on your map](#17-view-live-updates-on-your-map)

## Prerequisites
* Cloud
  * [Azure account](https://portal.azure.com/)
* IDE
  * Azure Funciton
    * [Visual Studio Community 2019](https://visualstudio.microsoft.com/zh-hant/vs/community/)  
  * Dashboard & Proxy
    * [Visual Studio Code](https://code.visualstudio.com/)
* Package and Language Version
  * Azure Funciton
    * Azure.Core v1.6.0
    * Azure.DigitalTwins.Core v1.2.0
    * Azure.Identity v1.3.0
    * Microsoft.Net.Sdk.Funtions v3.0.7
    * System.Net.Http v4.3.4
  * Dashboard & Proxy
    * [npm](https://www.npmjs.com/get-npm)
    * [Node.js v10.16.0](https://nodejs.org/en/download/)
    * [vue v2.6.12](https://vuejs.org/)
  * PnP
    * Python 3.7
      * azure-core 1.9.0
      * azure-eventhub 5.2.0
      * azure-iot-device 2.4.0
      * azure-iot-hub 2.2.3
      * async-timeout 3.0.1
      * cryptography 3.3.1
* CLI
  * [Azure CLI](https://docs.microsoft.com/zh-tw/cli/azure/install-azure-cli)
* API Client
  * [Postman](https://www.postman.com/)
* Drawing package
  * [AutoCAD](https://www.autodesk.com.tw/products/autocad/overview?term=1-YEAR)

## SOP for Initiating Services
### 1. Download Sample Code
* 1.1 Download project
  * https://github.com/ArcherHuang/Azure-Digital-Twins-for-Azure-Percept/tree/Azure-Percept
* 1.2 Click `Code` > `Download ZIP`
  ![](../Image/---2021-03-30---8.22.19.png)
* 1.3 Unzip `Azure-Digital-Twins-for-RPC-main.zip`
### 2. Install the Azure CLI and Login
* 2.1 Install the Azure CLI
  * [Reference documentation](https://docs.microsoft.com/zh-tw/cli/azure/install-azure-cli)
* 2.2 Sign in with Azure CLI
  * Run the login command
    ```
    az login
    ```
  * If the CLI can open your default browser, it will do so and load an Azure sign-in page. 
    * Sign in with your account credentials in the browser.
      ![](../Image/az-login-1.png)
    * Login Success
      * Browser
        ![](../Image/az-login-2.png)
      * Terminal
        ![](../Image/az-login-3.png)

### 3. Create a resource group
* Azure CLI
  ```
  az group create --name <ResourceGroup> --location <Region>
  ```
* e.g.
  ```
  az group create --name percept-adt-rg --location eastus
  ```
  * Execution Result
    ```
    {
      "id": "/subscriptions/oooooooo-oooo-oooo-oooo-oooooooooooo/resourceGroups/percept-adt-rg",
      "location": "eastus",
      "managedBy": null,
      "name": "percept-adt-rg",
      "properties": {
        "provisioningState": "Succeeded"
      },
      "tags": null,
      "type": "Microsoft.Resources/resourceGroups"
    }
    ```
### 4. Create Azure Digital Twin
* 4.1 Search `Azure Digital Twins`
  ![](../Image/---2021-03-29---1.18.12.png)

* 4.2 Select `Azure Digital Twins`
  ![](../Image/---2021-03-29---1.20.21.png)

* 4.3 Click `Add`
  ![](../Image/---2021-03-29---1.20.21-1.png)
  
* 4.4 Input data
  ![](../Image/---2021-03-29---1.24.25.png)
  * `Subscription` field
    * Select the subscription you want to use 
  * `Resource group` field
    * Use the `Resource Group` created in [step 3](#3-create-a-resource-group), this example uses `percept-adt-rg`
  * `Location` field
    * This example uses  `East US` 
  * `Resource name` field
    * Please use a recognizable name, this example uses `percept-adt-example`
* 4.5 When the input is complete, please click the `Review + create` button
  ![](../Image/create-adt-01.png)
* 4.6 Review your settings and click the `create` button
  ![](../Image/---2021-03-29---1.31.02.png)

* 4.7 Wait for the request to process
  ![](../Image/---2021-03-29---1.39.05.png)

* 4.8 Once deployment complete click the `Go to resource` button
  ![](../Image/---2021-03-29---1.31.59.png)
  
* 4.9 Set Access control
  * Click the `Access control (IAM)` button
    ![](../Image/adt-iam-1.png)
  * Click the `Add role assignments` button
    ![](../Image/adt-iam-2.png)
  * Input data
    ![](../Image/adt-iam-3.png)
    * `Role` field
      * Select the `Azure Digital Twins Data Owner`
    * `Select` field
      * Select you want to assign to the role for this resource
    * When the input is complete, please click the `Save` button
      ![](../Image/adt-iam-4.png)
  * Click the `View my access` button
    ![](../Image/adt-iam-5.png)
  * Execution Result
    ![](../Image/adt-iam-6.png)

* 4.10 Get `Azure Digital Twins Service URL`
  ![](../Image/---2021-03-30---8.34.37.png)

### 5. Set Azure AD for Azure Map
* 5.1 Open `Azure Active Directory`
  * 5.1.1 Search `ad`
    ![](../Image/ad-1.png)
  * 5.1.2 Select `Azure Active Directory`
    ![](../Image/ad-2.png)

* 5.2 Create App registrations
  * 5.2.1 Click `App registrations`
    ![](../Image/ad-3.png)
  * 5.2.2 Click `+ New registration`
    ![](../Image/ad-4.png)
  * 5.2.3 Input data
    ![](../Image/ad-5.png)
    * `Name` field
      * Please use a recognizable name, this example uses `percept-adt-demo`
    * `Supported account types` field
      * Select `Accounts in this organizational directory only (預設目錄 only - Single tenant)`
    * When the input is complete, please click the `Register` button
      ![](../Image/ad-6.png)

* 5.3 Authentication
  * 5.3.1 Click `Authentication`
    ![](../Image/ad-7.png)
  * 5.3.2 Click `+ Add a platform`
    ![](../Image/ad-8.png)
  * 5.3.3 Click `Web`
    ![](../Image/ad-9.png)
  * 5.3.4 Configure Web
    * `Redirect URIs` field
       * Please input `https://www.getpostman.com/oauth2/callback`
    * `Implicit grant and hybrid flows`
       * Select `Access tokens (used for implicit flows)`
    * When the input is complete, please click the `Configure` button
      ![](../Image/ad-10.png)

* 5.4 Set API permissions
  * Click `API permissions`
    ![](../Image/ad-20.png)
  * Click `Add a permissions`
    ![](../Image/ad-21.png)
  * Click `APIs my organization uses`
    ![](../Image/ad-22.png)
  * Search `Azure digital twin`
    ![](../Image/ad-23.png)
  * Click `Azure Digital Twins`
    ![](../Image/ad-24.png)
  * Click `Read.Write`
    ![](../Image/ad-25.png)
  * Click `Add permissions`
    ![](../Image/ad-26.png)
  * Click `Grant admin consent for 預設目錄`
    ![](../Image/ad-27.png)
  * Click `Yes`
    ![](../Image/ad-28.png)
  * Execution Result
    ![](../Image/ad-29.png)

* 5.5 Set `Authorization` in Postman
  * Download `Postman` and Install
    * https://www.postman.com/downloads/
  * Open `Postman` and Click `Authorization` tab
    ![](../Image/ad-11.png)
  * `Authorization` tab
    * `Type` field
      * Select `OAuth 2.0`
        ![](../Image/ad-12.png)
    * `Configure New Token`
      * `Grant Type` field
        * Select `Implicit`
      * `Callback URL` field
        * Please input `https://www.getpostman.com/oauth2/callback` 
      * `Auth URL` field
        * https://login.microsoftonline.com/TENANT_ID/oauth2/authorize?resource=0b07f429-9f4b-4714-9392-cc5e8e80c8b0
          * Modify `TENANT_ID` to `Directory (tenant) ID`
            ![](../Image/ad-13.png)
      * `Client ID` field
        ![](../Image/ad-14.png)
      * When the input is complete, please click the `Get New Access Token` button 
        ![](../Image/ad-15.png)
      * Click `Use Token`
        ![](../Image/ad-16.png)

### 6. Upload DWG & manifest.json to Azure Map using Postman
* 6.1 Create `Azure Maps Account`
  * 6.1.1 Search `map`
    ![](../Image/map-1.png)
  * 6.1.2 Select `Azure Maps Accounts`
    ![](../Image/map-2.png)
  * 6.1.3 Click `Add`
    ![](../Image/map-3.png)
  * 6.1.4 Input data
    ![](../Image/map-4.png)
    * `Subscription` field
      * Select the subscription you want to use
    * `Resource group` field
      * Use the `Resource Group` created in [step 3](#3-create-a-resource-group), this example uses `percept-adt-rg`
    * `Name` field
      * Please use a recognizable name, this example uses `percept-map`
    * `Pricing tier` field
      * this example uses `Standard S1`
    * `I confirm that I have read and agree to the License and Privacy Statement.` field
      * Please click `check`
    * When the input is complete, please click the `Create` button
      ![](../Image/map-5.png)
    * Once deployment complete click on `Go to resource` button
      ![](../Image/map-6.png)
  * 6.1.5 Get `subscription-key`
    * Click `Authentication`
      ![](../Image/map-7.png)
    * Get `Primary Key`
      ![](../Image/map-8.png)
  * 6.1.6 Create `Creator overview`
    * Click `Creator overview`
      ![](../Image/map-23.png)
    * Click `+ Create a Creator resource`
      ![](../Image/map-24.png)
    * Input data
      ![](../Image/map-25.png)
      * `Creator name` field
        * Please use a recognizable name, this example uses `percept-map-creator`
      * When the input is complete, please click the `Review + create` button
        ![](../Image/map-26.png)
      * Review your settings and click the `Create` button
        ![](../Image/map-27.png)
      * When the deployment completes, you'll see a page with a success or a failure message
        ![](../Image/map-28.png)
* 6.2 Download and install `Postman`
  * https://www.postman.com/downloads/
* 6.3 Upload a Drawing package to `Azure Map`
  * 6.3.1 Create Request
    * HTTP Method
      * POST
    * Request
      * https://atlas.microsoft.com/mapData/upload?api-version=1.0&dataFormat=zip&subscription-key=AZURE-MAPS-PRIMARY-KEY
      * Comment
        * Modify `AZURE-MAPS-PRIMARY-KEY` to `Primary Key`
          ![](../Image/map-key.png)
    * Headers
      * Content-Type: `application/octet-stream`
        ![](../Image/map-9.png)
    * Body
      * Select `binary`
      * Select File: Upload `./Azure-Digital-Twins-for-RPC/Indoor-Map-Files/Indoor-Map-Files.zip`
        ![](../Image/map-11.png)
        ![](../Image/map-10.png)
  * 6.3.2 Click the blue `Send` button and wait for the request to process
    ![](../Image/map-12.png)
  * 6.3.3 Request complete
    ![](../Image/map-13.png)
* 6.4 To check the status of the API call
  * 6.4.1 Go to the Headers tab of the response
    ![](../Image/map-14.png)
  * 6.4.2 Copy the value of the Location key
    ![](../Image/map-15.png)
  * 6.4.3 Need to append your primary subscription key to the URL for authentication
    * HTTP Method
      * GET
    * Request
      * `https://atlas.microsoft.com/mapData/operations/<operationId>?api-version=1.0&subscription-key=AZURE-MAPS-PRIMARY-KEY`
      * Comment
        * Modify `AZURE-MAPS-PRIMARY-KEY` to `Primary Key`
          ![](../Image/map-key.png)
  * 6.4.4 Click the blue `Send` button and wait for the request to process
    ![](../Image/map-20.png)
  * 6.4.5 Request complete
    ![](../Image/map-16.png)
* 6.5 To retrieve content metadata
  * 6.5.1 Copy the `resourceLocation` that was retrieved in `Step 6.4.5`
    ![](../Image/map-17.png)
  * 6.5.2 Need to append your primary subscription key to the URL for authentication
    * HTTP Method
      * GET
    * Request
      * https://atlas.microsoft.com/mapData/metadata/{udid}?api-version=1.0&subscription-key=AZURE-MAPS-PRIMARY-KEY
      * Comment
        * Modify `AZURE-MAPS-PRIMARY-KEY` to `Primary Key`
          ![](../Image/map-key.png)
  * 6.5.3 Click the blue `Send` button and wait for the request to process
    ![](../Image/map-21.png)
  * 6.5.4 Request complete
      ![](../Image/map-18.png)
* 6.6 Convert a Drawing package
  * 6.6.1 Create convert request
    * HTTP Method
      * POST
    * Request
      * https://atlas.microsoft.com/conversion/convert?subscription-key=AZURE-MAPS-PRIMARY-KEY&api-version=1.0&udid=UDID&inputType=DWG
      * Comment
        * 1. Modify `AZURE-MAPS-PRIMARY-KEY` to `Primary Key`
          ![](../Image/map-key.png)
        * 2. Modify `UDID` to `udid` that was retrieved in `Step 6.5.4`
    * Headers
      * Content-Type: `application/json`
        ![](../Image/map-19.png)
  * 6.6.2 Click the blue `Send` button and wait for the request to process
    ![](../Image/map-22.png)
  * 6.6.3 Request complete
    ![](../Image/map-29.png)
  * 6.6.4 Go to the Headers tab of the response, and look for the Location key
    ![](../Image/map-30.png)
  * 6.6.5 Copy the value of the Location key
    ![](../Image/map-31.png)
  * 6.6.6 Need to append your primary subscription key to the URL for authentication
    * HTTP Method
      * GET
    * Request
      * `https://atlas.microsoft.com/conversion/operations/<operationId>?api-version=1.0&subscription-key=AZURE-MAPS-PRIMARY-SUBSCRIPTION-KEY`
      * Comment
        * Modify `AZURE-MAPS-PRIMARY-SUBSCRIPTION-KEY` to `Primary Key`
          ![](../Image/map-key.png)
  * 6.6.7 Click the blue `Send` button and wait for the request to process
    ![](../Image/map-32.png)
  * 6.6.8 Request complete
      ![](../Image/map-33.png)
      * Comment
        * Copy the conversionId from the resourceLocation URL for the converted package. The conversionId is used by other API to access the converted map data.
          * https://atlas.microsoft.com/conversion/8648ea79-14c1-b00e-d898-4fed5c846474?api-version=1.0
          * https://atlas.microsoft.com/conversion/CONVERSIONID?api-version=1.0
* 6.7 Create a dataset
  * 6.7.1 Create dataset request
    * HTTP Method
      * POST
    * Request
      * https://atlas.microsoft.com/dataset/create?api-version=1.0&conversionID=CONVERSIONID&type=facility&subscription-key=AZURE-MAPS-PRIMARY-KEY
      * Comment
        * 1. Modify `AZURE-MAPS-PRIMARY-KEY` to `Primary Key`
          ![](../Image/map-key.png)
        * 2. Modify `CONVERSIONID` to `CONVERSIONID` that was retrieved in `Step 6.6.8`
  * 6.7.2 Click the blue `Send` button and wait for the request to process
    ![](../Image/map-34.png)
  * 6.7.3 Request complete
    ![](../Image/map-35.png)
  * 6.7.4 Get datasetId
    * Go to the Headers tab of the response
      ![](../Image/map-36.png)
    * Copy the value of the Location key
      ![](../Image/map-37.png)
    * Need to append your primary subscription key to the URL for authentication
      * HTTP Method
        * GET
      * Request
        * `https://atlas.microsoft.com/dataset/operations/<operationId>?api-version=1.0&subscription-key=AZURE-MAPS-PRIMARY-KEY`
        * Comment
          * Modify `AZURE-MAPS-PRIMARY-KEY` to `Primary Key`
            ![](../Image/map-key.png)
    * Click the blue `Send` button and wait for the request to process
      ![](../Image/map-38.png)
    * Request complete
      ![](../Image/map-39.png)
      * Comment
        * The response header will contain the DATASETID for the created dataset. Copy the DATASETID. You'll need to use the DATASETID to create a tileset.
          * `https://atlas.microsoft.com/dataset/9352e113-9133-b24b-64ee-adb5b9d92857?api-version=1.0`
          * `https://azure.microsoft.com/dataset/DATASETID?api-version=1.0`
* 6.8 Create a tileset
  * 6.8.1 Create tileset request
    * HTTP Method
      * POST
    * Request
      * https://atlas.microsoft.com/tileset/create/vector?api-version=1.0&datasetID=DATASETID&subscription-key=AZURE-MAPS-PRIMARY-KEY
      * Comment
        * 1. Modify `AZURE-MAPS-PRIMARY-KEY` to `Primary Key`
          ![](../Image/map-key.png)
        * 2. Modify `DATASETID` to `DATASETID` that was retrieved in `Step 6.7.4`
  * 6.8.2 Click the blue `Send` button and wait for the request to process
    ![](../Image/map-40.png)
  * 6.8.3 Request complete
    ![](../Image/map-41.png)
  * 6.8.4 Get tilesetId
    * Go to the Headers tab of the response
      ![](../Image/map-42.png)
    * Copy the value of the Location key
      ![](../Image/map-43.png)
    * Need to append your primary subscription key to the URL for authentication
      * HTTP Method
        * GET
      * Request
        * `https://atlas.microsoft.com/tileset/operations/<operationId>?api-version=1.0&subscription-key=AZURE-MAPS-PRIMARY-KEY`
        * Comment
          * Modify `AZURE-MAPS-PRIMARY-KEY` to `Primary Key`
            ![](../Image/map-key.png)
    * Click the blue `Send` button and wait for the request to process
      ![](../Image/map-44.png)
    * Request running
      ![](../Image/map-45.png)
    * Request complete
      ![](../Image/map-46.png) 
      * Comment
        * The response header will contain the TILESETID for the created dataset. Copy the TILESETID. You'll need to use the TILESETID to create a tileset.
          * `https://atlas.microsoft.com/tileset/35120fec-a07b-c6fa-49e2-cf30e23e2a6b?api-version=1.0`
          * `https://atlas.microsoft.com/tileset/TILESETID?api-version=1.0`
* 6.9 Query datasets with WFS API
  * 6.9.1 Make a GET request to view a list of the collections in the dataset
    * HTTP Method
      * GET
    * Request
      * https://atlas.microsoft.com/wfs/datasets/DATASETID/collections?subscription-key=AZURE-MAPS-PRIMARY-KEY&api-version=1.0
      * Comment
        * 1. Modify `AZURE-MAPS-PRIMARY-KEY` to `Primary Key`
          ![](../Image/map-key.png)
        * 2. Modify `DATASETID` to `DATASETID` that was retrieved in `Step 6.7.4`
  * 6.9.2 Click the blue `Send` button and wait for the request to process
    ![](../Image/map-47.png)
  * 6.9.3 Request complete
    ![](../Image/map-48.png)
* 6.10 Make a request for the unit feature collections
  * 6.10.1 Make a GET request
    * HTTP Method
      * GET
    * Request
      * https://atlas.microsoft.com/wfs/datasets/DATASETID/collections/unit/items?subscription-key=AZURE-MAPS-PRIMARY-KEY&api-version=1.0
      * Comment
        * 1. Modify `AZURE-MAPS-PRIMARY-KEY` to `Primary Key`
          ![](../Image/map-key.png)
        * 2. Modify `DATASETID` to `DATASETID` that was retrieved in `Step 6.7.4`
  * 6.10.2 Click the blue `Send` button and wait for the request to process
    ![](../Image/map-49.png)
  * 6.10.3 Request complete
    ![](../Image/map-50.png)
    * Comment
      * Copy the feature `id` for a unit feature, we'll use this feature id in the next section.
* 6.11 Create a feature stateset
  * 6.11.1 Make a POST request to the Create Stateset API
    * HTTP Method
      * POST
    * Request
      * https://atlas.microsoft.com/featureState/stateset?api-version=1.0&datasetId=DATASETID&subscription-key=AZURE-MAPS-PRIMARY-KEY
      * Comment
        * 1. Modify `AZURE-MAPS-PRIMARY-KEY` to `Primary Key`
          ![](../Image/map-key.png)
        * 2. Modify `DATASETID` to `DATASETID` that was retrieved in `Step 6.7.4`
    * Headers
      * Content-Type: `application/json`
        ![](../Image/map-54.png)
    * Body
      * raw: 
        ```
        {
          "styles":[
              {
                "keyname": "setAlarm",
                "type": "string",
                "rules": [
                    {
                      "alarm": "#FF0000",
                      "normal": "#00FF00",
                      "init": "#7DF9FF",
                      "no": "#d9e6f3",
                      "gray": "#E6E6E6"
                    }
                ]
              }
          ]
        }
        ```
        ![](../Image/map-51.png)
  * 6.11.2 Click the blue `Send` button and wait for the request to process
    ![](../Image/map-52.png)
  * 6.11.3 Request complete
    ![](../Image/map-53.png)
    * Comment
      * Copy the `statesetId` from the response body
* 6.12 Update the state
  * 6.12.1 Make a POST request to the Create Stateset API
    * HTTP Method
      * POST
    * Request
      * https://atlas.microsoft.com/featureState/state?api-version=1.0&statesetID=STATESETID&featureID=FEATUREID&subscription-key=AZURE-MAPS-PRIMARY-KEY
      * Comment
        * 1. Modify `AZURE-MAPS-PRIMARY-KEY` to `Primary Key`
          ![](../Image/map-key.png)
        * 2. Modify `STATESETID` to `statesetId` that was retrieved in `Step 6.11.3`
        * 3. Modify `FEATUREID` to `id` that was retrieved in `Step 6.10.3`
    * Headers
      * Content-Type: `application/json`
        ![](../Image/map-55.png)
    * Body
      * raw
        ```
        {
          "states": [
            {
                "keyName": "setAlarm",
                "value": "init",
                "eventTimestamp": "2021-03-31T11:39:01"
            }
          ]
        }
        ```
        ![](../Image/map-56.png)
      * Comment
        * The update will only be saved if the time posted stamp is after the time stamp of the previous request. 
  * 6.12.2 Click the blue `Send` button and wait for the request to process
    ![](../Image/map-57.png)
  * 6.12.3 Request complete
    ![](../Image/map-58.png)

### 7. Create & Deploy toADT Function
* 7.1 Create Azure Functions
  * Search `function`
    ![](../Image/---2021-03-30---10.34.09.png)
  * Select `Function App`
    ![](../Image/---2021-03-30---10.36.08.png)
  * Click `Add`
    ![](../Image/---2021-03-30---10.37.38.png)
  * Input data
    ![](../Image/---2021-03-30---10.39.16.png)
    * `Subscription` field
      * Select the subscription you want to use
    * `Resource group` field
      * Use the `Resource Group` created in [step 3](#3-create-a-resource-group), this example uses `percept-adt-rg`
    * `Function App name` field
      * Please use a recognizable name, this example uses `perceptIngestADTFunctions`
    * `Publish` field
      * Select `Code`
    * `Runtime stack` field
      * Select `.NET`
    * `Version` 欄位
      * Select `3.1`
    * `Region` field
      * This example uses  `East US`
    * When the input is complete, please click the `Review + create` button
      ![](../Image/---2021-03-30---10.43.10.png)

    * Review your settings and select `Create`
      ![](../Image/---2021-03-30---10.44.56.png)

    * Wait for the request to process
      ![](../Image/---2021-03-30---10.45.56.png)

    * Once deployment complete click on `Go to resource` button
      ![](../Image/---2021-03-30---10.47.16.png)

* 7.2 Set Configuration
  * Click `Configuration`
    ![](../Image/---2021-03-30---10.48.54.png)
  * Click `+ New application setting`
    ![](../Image/---2021-03-30---10.50.22.png)
  * Input data
    ![](../Image/---2021-03-30---10.52.34.png)
    * In the `Name` field, please enter `ADT_SERVICE_URL`
    * In the `Value` field ( Add prefix `https://` in URL )
      ![](../Image/adt-1.png)
    * Please click the `OK` button after entering the above information
      ![](../Image/---2021-03-30---10.53.14.png)
    * Click `Save`
      ![](../Image/---2021-03-30---10.55.02.png)
    * Click `Continue`
      ![](../Image/---2021-03-30---10.55.56.png)
* 7.3 Assign access role
  * Select `Identity` in the navigation bar on the left to work with a managed identity for the function
    ![](../Image/identity-1.png)
  * Click the `On` button
    ![](../Image/identity-2.png)
  * Click the `Save` button
    ![](../Image/identity-3.png)
  * Click the `Yes` button
    ![](../Image/identity-4.png)
  * Click the `Azure role assignments` button
    ![](../Image/identity-5.png)
  * Click the `+ Add role assignment (Preview)` button
    ![](../Image/identity-6.png)
  * Input data
    ![](../Image/identity-7.png)
    * `Scope`: Select `Resource group`
    * `Subscription`: Select your Azure subscription
    * `Resource group`: Select your resource group from the dropdown
    * `Role`: Select `Azure Digital Twins Data Owner` from the dropdown
    * When the input is complete, please click the `Save` button
      ![](../Image/identity-8.png)
    * Save finish
      ![](../Image/identity-9.png)

* 7.4 Opening `IngestADTFunctions.sln` from `/Back-End/Azure-Functions/IngestADTFunctions` in `Visual Studio 2019`
  ![](../Image/IngestADTFunctions-1.png)
  ![](../Image/IngestADTFunctions-2.png)

* 7.5 Build `IngestADTFunctions`
  * Click `Build`
    ![](../Image/IngestADTFunctions-31.png)
  * Execution Result
    ![](../Image/IngestADTFunctions-32.png)

* 7.6 Deploy `IngestADTFunctions` to `Azure Function`
  * Click `Publish...`
    ![](../Image/IngestADTFunctions-3.png)
  * Click `+ New`
    ![](../Image/IngestADTFunctions-4.png)
  * Click `Azure`
  
    ![](../Image/IngestADTFunctions-5.png)
  * Click `Azure Function App (Windows)` > `Next`
    ![](../Image/IngestADTFunctions-6.png)
  * Please select the function created in [`Step 7.1`](#7-create--deploy-toadt-function) and click the `Finish` button
    ![](../Image/IngestADTFunctions-7.png)
  * Click `Publish`
    ![](../Image/IngestADTFunctions-8.png)
  * Execution Result
    ![](../Image/IngestADTFunctions-9.png)

### 8. Create Azure IoT Hub, Set Event Grid, Create IoT Device
* 8.1 Search `iot hub`
  ![](../Image/---2021-03-29---4.12.49.png)

* 8.2 Select `IoT Hub`
  ![](../Image/---2021-03-29---4.13.39.png)

* 8.3 Click `+ Add`
  ![](../Image/---2021-03-29---4.14.31.png)
  
* 8.4 Input data
  ![](../Image/---2021-03-29---4.15.48.png)
  * `Subscription` field
    * Select the subscription you want to use
  * `Resource group` field
    * Use the `Resource Group` created in [step 3](#3-create-a-resource-group), this example uses `percept-adt-rg`
  * `Region` field
    * This example uses `East US`
  * `IoT hub name` field
    * Please use a recognizable name, this example uses `percept-adt-hub`
* 8.5 When the input is complete, please click the `Review + create` button
  ![](../Image/---2021-03-29---4.18.51.png)
* 8.6 Review your settings and click the `create` button
  ![](../Image/---2021-03-29---4.19.24.png)

* 8.7 Wait for the request to process
  ![](../Image/---2021-03-29---4.20.32.png)
  
* 8.8 Operation completes and click the `Go to resource` button
  ![](../Image/---2021-03-29---4.23.23.png)
* 8.9 Set Event to `IngestADTFunctions` Azure Function
  * Click `Events`
    ![](../Image/hub-evnet-1.png)
  * Click `+ Event Subscription`
    ![](../Image/hub-evnet-2.png)
  * Input data
    ![](../Image/hub-evnet-3.png)
    * `Name` field
      * Please use a recognizable name, this example uses `adtEvent`
    * `System Topic Name` field
      * Please use a recognizable name, this example uses `test`
    * `Filter to Event Types` field
      * Please select `Device Created`、`Device Deleted`、`Device Connected`、`Device Disconnected`、`Device Telemetry`
    * `Endpoint Type` field
      * Please select `Azure Function`
    * `Endpoint` field
      * Please select `Select an endpoint`
      * `Select Azure Function` View
        * `Subscription` field
          * Select the subscription you want to use
        * `Resource group` field
          * Select your resource group from the dropdown, this example uses `percept-adt-rg`
        * `Function app` field
          * Select your azure function from the dropdown, this example uses `IngestADTFunctions`
        * `Slot` field
          * Please select `Production`
        * `Function` field
          * Please select `Function1`
        * When the input is complete, please click the `Confirm Selection` button
          ![](../Image/hub-evnet-4.png)
    * When the input is complete, please click the `Create` button
      ![](../Image/hub-evnet-5.png)
* 8.10 Create IoT Devices
  * Click `IoT Devices` 
    ![](../Image/iot-hub-4.png)
  * Click `+ New` 
    ![](../Image/iot-hub-5.png)
  * Input data
    ![](../Image/iot-hub-6.png)
    * `Device ID` field
      * Input `percept-dt-001`
    * When the input is complete, please click the `Save` button
      ![](../Image/iot-hub-7.png)
### 9. Set Event & toTsi Function
* 9.1 Create an event hub namespace that will receive events from your Azure Digital Twins instance
  * Azure CLI
    ```
    az eventhubs namespace create --name <name for your Event Hubs namespace> --resource-group <resource group name> -l <region>
    ```
  * e.g.
    ```
    az eventhubs namespace create --name percepthubspace --resource-group percept-adt-rg -l eastus
    ```
* 9.2 Create an event hub within the namespace to receive twin change events. Specify a name for the event hub.
  * Azure CLI
    ```
    az eventhubs eventhub create --name <name for your Twins event hub> --resource-group <resource group name> --namespace-name <Event Hubs namespace from above>
    ```
  * e.g.
    ```
    az eventhubs eventhub create --name perceptadteventhub --resource-group percept-adt-rg --namespace-name percepthubspace
    ```
* 9.3 Create an authorization rule with send and receive permissions. Specify a name for the rule.
  * Azure CLI
    ```
    az eventhubs eventhub authorization-rule create --rights Listen Send --resource-group <resource group name> --namespace-name <Event Hubs namespace from above> --eventhub-name <Twins event hub name from above> --name <name for your Twins auth rule>
    ```
  * e.g.
    ```
    az eventhubs eventhub authorization-rule create --rights Listen Send --resource-group percept-adt-rg --namespace-name percepthubspace --eventhub-name perceptadteventhub --name perceptadteventrules
    ```
* 9.4 Create an Azure Digital Twins endpoint that links your event hub to your Azure Digital Twins instance.
  * Azure CLI
    ```
    az dt endpoint create eventhub -n <your Azure Digital Twins instance name> --endpoint-name <name for your Event Hubs endpoint> --eventhub-resource-group <resource group name> --eventhub-namespace <Event Hubs namespace from above> --eventhub <Twins event hub name from above> --eventhub-policy <Twins auth rule from above>
    ```
  * e.g.
    ```
    az dt endpoint create eventhub --endpoint-name percepthubadtendpoint --eventhub-resource-group percept-adt-rg --eventhub-namespace percepthubspace --eventhub perceptadteventhub --eventhub-policy perceptadteventrules -n percept-adt-example --resource-group percept-adt-rg
    ```
* 9.5 Create a route in Azure Digital Twins to send twin update events to your endpoint. The filter in this route will only allow twin update messages to be passed to your endpoint.
  * Azure CLI
    ```
    az dt route create -n <your Azure Digital Twins instance name> --endpoint-name <Event Hub endpoint from above> --route-name <name for your route> --filter "type = 'Microsoft.DigitalTwins.Twin.Update'"
    ```
  * e.g.
    ```
    az dt route create -n percept-adt-example --endpoint-name percepthubadtendpoint --route-name perceptroutename --filter "type = 'Microsoft.DigitalTwins.Twin.Update'" --resource-group percept-adt-rg
    ```
* 9.6 Create & Deploy a function in Azure
  * 9.6.1 Create Azure Functions
    * Search `function`
      ![](../Image/---2021-03-30---10.34.09.png)
    * Select `Function App`
      ![](../Image/---2021-03-30---10.36.08.png)
    * Click `Add`
      ![](../Image/---2021-03-30---10.37.38.png)
    * Input data
      ![](../Image/---2021-03-30---10.39.16.png)
      * `Subscription` field
        * Select the subscription you want to use 
      * `Resource group` field
        * Use the `Resource Group` created in [step 3](#3-create-a-resource-group), this example uses `percept-adt-rg`
      * `Function App name` field
        * Please use a recognizable name, this example uses `perceptEmitAdtTsiFunctions`
      * `Publish` field
        * Select `Code`
      * `Runtime stack` field
        * Select `.NET`
      * `Version` field
        * Select `3.1`
      * `Region` field
        * This example uses `East US`
      * When the input is complete, please click the `Review + create` button
        ![](../Image/---2021-03-30---11.22.05.png)

      * Review your settings and select `Create`
        ![](../Image/---2021-03-30---11.23.02.png)

      * wait for the request to process
        ![](../Image/---2021-03-30---11.24.34.png)
      * Once deployment complete click on `Go to resource` button
        ![](../Image/---2021-03-30---11.25.21.png)

  * 9.6.2 Deploy
    * Opening `EmitAdtTsi.sln` from `/Back-End/Azure-Functions/EmitAdtTsi` in `Visual Studio 2019`
      ![](../Image/EmitAdtTsi-1.png)
      ![](../Image/EmitAdtTsi-2.png)
    * Build `EmitAdtTsi`
      * Click `Build`
        ![](../Image/EmitAdtTsi-31.png)
      * Execution Result
        ![](../Image/EmitAdtTsi-32.png)
    * Deploy `EmitAdtTsi` to `Azure Function`
      * Click `Publish...`
        ![](../Image/EmitAdtTsi-3.png)
      * Click `+ New`
        ![](../Image/EmitAdtTsi-4.png)
      * Click `Azure`

        ![](../Image/IngestADTFunctions-5.png)
      * Click `Azure Function App (Windows)` > `Next`
        ![](../Image/IngestADTFunctions-6.png)
      * Please select the function created in `Step 9.6.1`
        ![](../Image/EmitAdtTsi-7.png)
      * Click `Publish`
        ![](../Image/EmitAdtTsi-8.png)
      * Operation completes
        ![](../Image/EmitAdtTsi-9.png)
  
* 9.7 Create a new event hub. Specify a name for the event hub.
  * Azure CLI
    ```
    az eventhubs eventhub create --name <name for your TSI event hub> --resource-group <resource group name from earlier> --namespace-name <Event Hubs namespace from earlier>
    ```
  * e.g.
    ```
    az eventhubs eventhub create --name percepttsieventhub --resource-group percept-adt-rg --namespace-name percepthubspace
    ```
* 9.8 Create an authorization rule with send and receive permissions. Specify a name for the rule.
  * Azure CLI
    ```
    az eventhubs eventhub authorization-rule create --rights Listen Send --resource-group <resource group name> --namespace-name <Event Hubs namespace from earlier> --eventhub-name <TSI event hub name from above> --name <name for your TSI auth rule>
    ```
  * e.g.
    ```
    az eventhubs eventhub authorization-rule create --rights Listen Send --resource-group percept-adt-rg --namespace-name percepthubspace --eventhub-name percepttsieventhub --name percepttsieventrules
    ```
* 9.9 Get `Twins event hub connection string` ( primaryConnectionString )
  * Azure CLI
    ```
    az eventhubs eventhub authorization-rule keys list --resource-group <resource group name> --namespace-name <Event Hubs namespace> --eventhub-name <Twins event hub name> --name <Twins auth rule>
    ```
  * e.g.
    ```
    az eventhubs eventhub authorization-rule keys list --resource-group percept-adt-rg --namespace-name percepthubspace --eventhub-name perceptadteventhub --name perceptadteventrules
    ```
  * Result ( To get `primaryConnectionString` )
    ```
    {
      "aliasPrimaryConnectionString": null,
      "aliasSecondaryConnectionString": null,
      "keyName": "perceptadteventrules",
      "primaryConnectionString": "Endpoint=sb://percepthubspace.servicebus.windows.net/;SharedAccessKeyName=perceptadteventrules;SharedAccessKey=r/LfTCNF+iIwV663doQ6AuOS39DxDwv8wqYTNbi358o=;EntityPath=perceptadteventhub",
      "primaryKey": "r/LfTCNF+iIwV663doQ6AuOS39DxDwv8wqYTNbi358o=",
      "secondaryConnectionString": "Endpoint=sb://percepthubspace.servicebus.windows.net/;SharedAccessKeyName=perceptadteventrules;SharedAccessKey=otonMKbANlwKtrJG5+4VCJDujvdeYBIhhvPTxFVTv+c=;EntityPath=perceptadteventhub",
      "secondaryKey": "otonMKbANlwKtrJG5+4VCJDujvdeYBIhhvPTxFVTv+c="
    }
    ```  

* 9.10 Use the `primaryConnectionString` value from the result to create an app setting in your function app that contains your connection string:
  * Azure CLI
    ```
    az functionapp config appsettings set --settings "EventHubAppSetting-Twins=<Twins event hub connection string>" -g <resource group> -n <your App Service (function app) name>
    ```
  * e.g.
    ```
    az functionapp config appsettings set --settings "EventHubAppSetting-Twins=Endpoint=sb://percepthubspace.servicebus.windows.net/;SharedAccessKeyName=perceptadteventrules;SharedAccessKey=r/LfTCNF+iIwV663doQ6AuOS39DxDwv8wqYTNbi358o=;EntityPath=perceptadteventhub" -g percept-adt-rg -n perceptEmitAdtTsiFunctions
    ```
* 9.11 Get `TSI event hub connection string` ( primaryConnectionString )
  * Azure CLI
    ```
    az eventhubs eventhub authorization-rule keys list --resource-group <resource group name> --namespace-name <Event Hubs namespace> --eventhub-name <TSI event hub name> --name <TSI auth rule>
    ```
  * e.g.
    ```
    az eventhubs eventhub authorization-rule keys list --resource-group percept-adt-rg --namespace-name percepthubspace --eventhub-name percepttsieventhub --name percepttsieventrules
    ```
  * Result ( To get `primaryConnectionString` )
    ```
    {
      "aliasPrimaryConnectionString": null,
      "aliasSecondaryConnectionString": null,
      "keyName": "percepttsieventrules",
      "primaryConnectionString": "Endpoint=sb://percepthubspace.servicebus.windows.net/;SharedAccessKeyName=percepttsieventrules;SharedAccessKey=FO6aWgNfgw8HVspgqltzQh5zZQ9DvIhAWNDBzybMJFA=;EntityPath=percepttsieventhub",
      "primaryKey": "FO6aWgNfgw8HVspgqltzQh5zZQ9DvIhAWNDBzybMJFA=",
      "secondaryConnectionString": "Endpoint=sb://percepthubspace.servicebus.windows.net/;SharedAccessKeyName=percepttsieventrules;SharedAccessKey=Z4kfI0ppZQ1RNmGLr7irC3fKkeJKRmhRaLmDJOP7k30=;EntityPath=percepttsieventhub",
      "secondaryKey": "Z4kfI0ppZQ1RNmGLr7irC3fKkeJKRmhRaLmDJOP7k30="
    }
    ```

* 9.12 Use the `primaryConnectionString` value from the result to create an app setting in your function app that contains your connection string
  * Azure CLI
    ```
    az functionapp config appsettings set --settings "EventHubAppSetting-TSI=<TSI event hub connection string>" -g <resource group> -n <your App Service (function app) name>
    ```
  * e.g.
    ```
    az functionapp config appsettings set --settings "EventHubAppSetting-TSI=Endpoint=sb://percepthubspace.servicebus.windows.net/;SharedAccessKeyName=percepttsieventrules;SharedAccessKey=FO6aWgNfgw8HVspgqltzQh5zZQ9DvIhAWNDBzybMJFA=;EntityPath=percepttsieventhub" -g percept-adt-rg -n perceptEmitAdtTsiFunctions
    ```

* 9.13 Create `Consumer groups` of rptsieventhub
  * Search `event hub` and select the `Event Hubs`
    ![](../Image/tsi-evnet-01.png)
  * Please select the Event Hub created in `Step 9.1`
    ![](../Image/tsi-evnet-02.png)
  * Click the `Event Hubs` button
    ![](../Image/tsi-evnet-03.png)
  * Please select the Event Hub created in `Step 9.7`
    ![](../Image/tsi-evnet-04.png)
  * Click the `Consumer groups` button
    ![](../Image/tsi-event-hub-consumer-groups-view.png)
  * Click `+ Consumer groups`
    ![](../Image/tsi-event-hub-consumer-groups-add.png)
  * Input data
    ![](../Image/tsi-event-hub-consumer-groups-input.png)
    * `Name` field
      * Please use a recognizable name, this example uses `percept-pnp-resourcegroup`
    * When the input is complete, please click the `Create` button
      ![](../Image/tsi-event-hub-consumer-groups-input-create.png)
  * Operation completes
    ![](../Image/tsi-event-hub-consumer-groups-view2.png)

### 10. Create and set TSI Service
* 10.1 Create and connect a Time Series Insights instance
  * Search `time series insights`
    ![](../Image/tsi-serch-1.png)
  * Select `Time Series Insights environments`
    ![](../Image/tsi-serch-2.png)
  * Click `+ Add`
    ![](../Image/tsi-add.png)
  * Input data
    * Basics
      ![](../Image/tsi-input-1.png)
      ![](../Image/tsi-input-2.png)
      * `Subscription` field
        * Select the subscription you want to use
      * `Resource group` field
        * Use the `Resource Group` created in [step 3](#3-create-a-resource-group), this example uses `percept-adt-rg`
      * `Environment name` field
        * Please use a recognizable name, this example uses `percept-tsi`
      * `Location` field
        * This example uses `East US`
      * `Tier` field
        * This example uses `Gen2 (L1)`
      * `Property name` field
        * Please use a recognizable name, this example uses `ADTid`、`Timestamp`
      * `Storage account name` field
        * Please use a recognizable name, this example uses `percepttsi`
      * `Storage account kind` field
        * This example uses `StorageV2 (general purpose v2)`
      * `Storage account replication` field
        * This example uses `Locally redundant storage (LRS)`
      * `Hierarchial namespace` field
        * This example uses `Disabled`
      * `Enable warm store` field
        * This example uses `No`
    * Event Source
      ![](../Image/tsi-event-source-1.png)
      * `Create an event source?` field
        * This example uses `Yes`
      * `Source type` field
        * Select `Event Hub`
      * `Name` field
        * This example uses `percept-tsi-event-hub`
      * `Subscription` field
        * Select the subscription you want to use
      * `Event Hub namespace` field
        * Please select the `Endpoint` created in [`Step 9.1`](#9-set-event--totsi-function) (percepthubspace)
      * `Event Hub name` field
        * Please select the `TSI Event Hub` created in `Step 9.7` (percepttsieventhub)
      * `Event Hub access policy name` field
        * Please select the `Shared access policies` created in `Step 9.8` (percepttsieventrules)
      * `Event Hub consumer group` field
        * Please select the `Consumer groups` created in `Step 9.15` (percept-pnp-resourcegroup)
    * When the input is complete, please click the `Review + create` button
      ![](../Image/tsi-event-source-20.png)
      ![](../Image/tsi-event-source-21.png)
      ![](../Image/tsi-event-source-2.png)
    * Review your settings and select `Review + create`
      ![](../Image/tsi-event-source-30.png)
      ![](../Image/tsi-event-source-3.png)
  * wait for the request to process
    ![](../Image/tsi-event-source-4.png)
  * Execution Result
    ![](../Image/tsi-event-source-5.png)

### 11. Set Event & toMap Function
* 11.1 Create a route and filter to twin update notifications
  * Create an event grid topic, which will receive events from your Azure Digital Twins instance.
    * Azure CLI
      ```
      az eventgrid topic create -g <your-resource-group-name> --name <your-topic-name> -l <region>
      ```

    * e.g.
      ```
      az eventgrid topic create -g percept-adt-rg --name perceptmap -l eastus
      ```
  * Create an endpoint to link your event grid topic to Azure Digital Twins.
    * Azure CLI
      ```
      az dt endpoint create eventgrid --endpoint-name <Event-Grid-endpoint-name> --eventgrid-resource-group <Event-Grid-resource-group-name> --eventgrid-topic <your-Event-Grid-topic-name> -n <your-Azure-Digital-Twins-instance-name> --resource-group <resource group name>
      ```

    * e.g.
      ```
      az dt endpoint create eventgrid --endpoint-name perceptadteventgridmap --eventgrid-resource-group percept-adt-rg --eventgrid-topic perceptmap -n percept-adt-example --resource-group percept-adt-rg
      ```
  * Create a route in Azure Digital Twins to send twin update events to your endpoint.
    * Azure CLI
      ```
      az dt route create -n <your-Azure-Digital-Twins-instance-name> --endpoint-name <Event-Grid-endpoint-name> --route-name <my_route> --filter "type = 'Microsoft.DigitalTwins.Twin.Update'" --resource-group <resource group name>
      ```

    * e.g.
      ```
      az dt route create -n percept-adt-example --endpoint-name perceptadteventgridmap --route-name perceptadtmaproute --filter "type = 'Microsoft.DigitalTwins.Twin.Update'" --resource-group percept-adt-rg
      ```

* 11.2 Create & Deploy a function in Azure
  * 11.2.1 Create Azure Functions
    * Search `function`
      ![](../Image/---2021-03-30---10.34.09.png)
    * Select `Function App`
      ![](../Image/---2021-03-30---10.36.08.png)
    * Click `+ Add`
      ![](../Image/---2021-03-30---10.37.38.png)
    * Input data
      ![](../Image/---2021-03-30---10.39.16.png)
      * `Subscription` field
        * Select the subscription you want to use
      * `Resource group` field
        * Use the `Resource Group` created in [step 3](#3-create-a-resource-group), this example uses `percept-adt-rg`
      * `Function App name` field
        * Please use a recognizable name, this example uses `perceptToMapFunctions`
      * `Publish` field
        * Select `Code`
      * `Runtime stack` field
        * Select `.NET`
      * `Version` field
        * Select `3.1`
      * `Region` field
        * This example uses `East US`
      * Click on the `Review + create` button
        ![](../Image/map-59.png)
      * Review all the details and click on the `Create` button
        ![](../Image/map-60.png)
      * wait for the request to process
        ![](../Image/map-61.png)
      * Once deployment complete click on `Go to resource` button
        ![](../Image/map-62.png)

  * 11.2.2 Deploy
    * Opening `toMap.sln` from `/Back-End/Azure-Functions/toMap` in `Visual Studio 2019`
      ![](../Image/toMap-1.png)
      ![](../Image/toMap-2.png)
    * Build `toMap`
      * Click `Build`
        ![](../Image/toMap-31.png)
      * Execution Result
        ![](../Image/toMap-32.png)
    * Deploy `toMap` to `Azure Function`
      * Click `Publish...`
        ![](../Image/toMap-3.png)
      * Click `+ New`
        ![](../Image/toMap-4.png)
      * Click `Azure`

        ![](../Image/IngestADTFunctions-5.png)
      * Click `Azure Function App (Windows)` > `Next`
        ![](../Image/IngestADTFunctions-6.png)
      * Please select the function created in `Step 11.2.1`
        ![](../Image/toMap-7.png)
      * Click `Publish`
        ![](../Image/toMap-8.png)
      * Execution Result
        ![](../Image/toMap-9.png)

  * 11.2.3 Set Configuration
    * Azure Maps primary key
      * Azure CLI
        ```
        az functionapp config appsettings set --name <your-App-Service-(function-app)-name> --resource-group <your-resource-group> --settings "subscription-key=<your-Azure-Maps-primary-key>"
        ```

        * Get `Azure Maps Primary Key`
          ![](../Image/map-8.png)

      * e.g.
        ```
        az functionapp config appsettings set --name perceptToMapFunctions --resource-group percept-adt-rg --settings "subscription-key=KV67NoQW5AEkFfs1jDsj2sFKjSkM9UMEAJVZuc7f-9E"
        ``` 

    * Azure Maps stateset ID
      * Azure CLI
        ```
        az functionapp config appsettings set --name <your-App-Service-(function-app)-name>  --resource-group <your-resource-group> --settings "statesetID=<your-Azure-Maps-stateset-ID>"
        ```

        * Azure Maps stateset ID
          * Ref `Step 6.11.3`

      * e.g.
        ```
        az functionapp config appsettings set --name perceptToMapFunctions --resource-group percept-adt-rg --settings "statesetID=0696c4f7-f6c9-f5d0-8bdf-ed71d50f56f5"
        ```
  * 11.2.4 Set Event Subscription
    * Search `event grid topics` and Select
      ![](../Image/event-grid-topic-1.png)
    * Select topic
      * Use the event grid topic created in `step 11.1`
        ![](../Image/event-grid-topic-2.png)
    * Click `+ Event Subscription`
      ![](../Image/rpcmap-1.png)
    * Input data
      ![](../Image/rpcmap-2.png)
      * `Name` field
        * Please use a recognizable name, this example uses `percept-event-grid-map`
      * `Endpoint Type` field
        * Select `Azure Function`
      * `Endpoint` field
        * Click `Select an endpoint`
        * `Select Azure Function` view
          ![](../Image/rpcmap-3.png)
          * `Subscription` field
            * Select the subscription you want to use
          * `Resource group` field
            * Please select the `resource group` created in `Step 3`
          * `Function app` field
            * Please select the function created in `Step 11.2`
          * `Slot` field
            * Select `Production`
          * `Function` field
            * Select `Function1`
          * When the input is complete, please click the `Confirm Selection` button
            ![](../Image/rpcmap-4.png)
      * When the input is complete, please click the `Create` button
        ![](../Image/rpcmap-5.png)

### 12. Set Dashboard and Upload Model
* 12.1 Install Node.js, npm and Vue on the local server
  * [npm](https://www.npmjs.com/get-npm)
  * [Node.js v10.16.0](https://nodejs.org/en/download/)
  * [vue v2.6.12](https://vuejs.org/)

* 12.2 Proxy Server
  * Enter the project folder
    ```
    cd ./Azure-Digital-Twins-for-RPC/Back-End/Proxy
    ```
  * Install packages via npm
    ```
    npm install
    ```
  * Create .env file
    ```
    touch .env
    ```
  * Store Key in .env file and save
    * Add ./Azure-Digital-Twins-for-RPC/Back-End/Proxy/.env content
      ```
      AZURE_DIGITAL_TWINS_HOST_NAME=https://
      ```
    * Comment
      * Get `Azure Digital Twins Service URL`
        ![](../Image/---2021-03-30---8.34.37.png)
  
  * Activate the server
    ```
    $ node index.js
    ```
  * Find the message for successful activation
    ```
    [HPM] Proxy created: /  -> https://percept-adt-example.api.eus.digitaltwins.azure.net
    Example app listening on port 3000!
    ```

* 12.3 Dashboard Server
  * Enter the project folder
    ```
    cd ./Azure-Digital-Twins-for-RPC/Front-End
    ```
  * Install packages via npm
    ```
    npm install
    ```
  * Create .env file
    ```
    touch .env
    ```
  * Create .env file
    * Add ./Azure-Digital-Twins-for-RPC/Front-End/.env content
      ```
      VUE_APP_MAP_SUBSCRIPTION_KEY=
      VUE_APP_MAP_TILESETID=
      VUE_APP_MAP_STATESETID=
      VUE_APP_LONGITUDE=
      VUE_APP_LATITUDE=
      VUE_APP_COMPANY_NAME=
      VUE_APP_EVENT_HUB_CONNECTIONSTRING=
      VUE_APP_EVENT_HUB_NAME=
      VUE_APP_IOT_HUB_ENDPOINT=
      VUE_APP_IOT_HUB_DEVICEKEY=
      VUE_APP_IOT_HUB_POLICYNAME=
      ```
    * Comment
      * VUE_APP_MAP_SUBSCRIPTION_KEY
        ![](../Image/map-8.png)
      * VUE_APP_MAP_TILESETID was retrieved in `Step 6.8.4`
      * VUE_APP_MAP_STATESETID was retrieved in `Step 6.11.3`
      * VUE_APP_EVENT_HUB_CONNECTIONSTRING
        ![](../Image/env-2.png)
      * VUE_APP_EVENT_HUB_NAME
        ![](../Image/env-3.png)
      * VUE_APP_IOT_HUB_ENDPOINT
        ![](../Image/env-4.png)
      * VUE_APP_IOT_HUB_DEVICEKEY & VUE_APP_IOT_HUB_POLICYNAME
        ![](../Image/env-5.png)

  * Activate the server
    ```
    npm run serve
    ```
  * Find the message for successful activation
    ```
    App running at:
    - Local:   http://localhost:8081/ 
    - Network: http://172.20.10.2:8081/

    Note that the development build is not optimized.
    To create a production build, run npm run build.
    ```
    ![](../Image/ui-1.png)

* 12.4 Upload DTDL
  * Open Dashboard
    ![](../Image/ui-2.png)
  * Upload floor-v3.json
    * Click `Upload Model`
      ![](../Image/ui-3.png)
    * Click `Browse`
      ![](../Image/ui-4.png)
    * Select `./Azure-Digital-Twins-for-RPC/DTDL-Model/floor-v4.json`
      ![](../Image/ui-5.png)
    * Click `Submit`
      ![](../Image/ui-6.png)
    * Upload finish
      ![](../Image/ui-7.png)
  * Upload room-v4.json
    * Click `Upload Model`
      ![](../Image/ui-80.png)
    * Click `Browse`
      ![](../Image/ui-4.png)
    * Select `./Azure-Digital-Twins-for-RPC/DTDL-Model/room-v4.json`
      ![](../Image/ui-8.png)
    * Click `Submit`
      ![](../Image/ui-6.png)
    * Upload finish
      ![](../Image/ui-9.png)
  * peceptorStats-v1.json
    * Click `Upload Model`
      ![](../Image/ui-101.png)
    * Click `Browse`
      ![](../Image/ui-4.png)
    * Select `./Azure-Digital-Twins-for-RPC/DTDL-Model/peceptorStats-v1.json`
      ![](../Image/ui-10.png)
    * Click `Submit`
    * Upload finish
      ![](../Image/ui-11.png)

### 13. Start Device by running percept_pnp.py
* 13.1 Add `IoT Devices`
  * Search `iot hub`
    ![](../Image/iot-hub-1.png)
  * Select `IoT Hub`
    ![](../Image/iot-hub-2.png)
  * Click on the `IoT Hub` created in `Step 8.4`
    ![](../Image/iot-hub-3.png)
  * Click `IoT Devices` 
    ![](../Image/iot-hub-4.png)
  * Click `+ New` 
    ![](../Image/iot-hub-5.png)
  * Input data
    ![](../Image/iot-hub-6.png)
    * `Device ID` field
      * Input `percept-dt-001`
    * When the input is complete, please click the `Save` button
      ![](../Image/iot-hub-7.png)
  * Click `percept-dt-001`
    ![](../Image/iot-hub-8.png)
  * Get `Connection String`
    ![](../Image/iot-hub-9.png)
* 13.2 Install Python 3.7.0 on the Plug and Play Device
  * [Download And Install](https://www.python.org/downloads/release/python-370/)
* 13.3 Install Package on the Plug and Play Device
  * Enter the project folder
    ```
    cd ./Azure-Digital-Twins-for-RPC/PnP-Device/Percept
    ```
  * Install
    ```
    pip install -r requirements.txt
    ```
* 13.4 Run code on the Plug and Play Device
  * Change values in percept_pnp.py
    * Device ID
      ```
      rpc_component_name_01 = 'percept-dt-001'
      ```
      ![](../Image/iot-hub-8.png)
    * IoT Hub connection string
      ```
      IOTHUB_CONNECTION_STRING=""
      ```
      ![](../Image/iot-hub-91.png)
    * IoT Hub Device connection string
      ```
      IOTHUB_DEVICE_CONNECTION_STRING_DEV=";SharedAccessKeyName=iothubowner"
      ```
      ![](../Image/iot-hub-9.png)

### 14. Create Twin
* 14.1 Click `Outdoor Map`
  ![](../Image/create-twin-1.png)
* 14.2 Click `微軟`
  ![](../Image/create-twin-2.png)
* 14.3 Click `301`
  ![](../Image/create-twin-3.png)
* 14.4 Click `Add Device`
  ![](../Image/create-twin-4.png)
* 14.5 PnP Terminal
  ![](../Image/create-twin-5.png)

### 15. Visualize your data in Time Series Insights
* 15.1 Run percept_pnp.py
  * Enter the project folder
    ```
    cd ./Azure-Digital-Twins-for-RPC/PnP-Device/Percept
    ```
  * Run
    ```
    python3 percept_pnp.py
    ```
* 15.2 Get to TSI Explorer
  ![](../Image/tsi-event-source-6.png)
* 15.3 TSI Explorer View
  ![](../Image/tsi-event-source-7.png)
  ![](../Image/tsi-event-source-8.png)

### 16. View live updates on your dashboard
* Click `Tree Graph`
  ![](../Image/tree-graph-2.png)

### 17. View live updates on your map
* Alarm
  ![](../Image/map-result-1.png)
