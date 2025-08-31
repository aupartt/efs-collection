# Manage Grafana Dashboards

While there is a feature to sync Grafana provisioned dashboards, data sources, and more, directly with a GitHub repo, it (GitSync plugin) is still in heavy testing and not yet fully integrated.
- That's why we are versioning dashboards manually for now.

## 🗄️ Dashboards structure
In this repo all Dashboards files are located in the folder `./grafana/dashboards/` and use following syntax: `<dashboard-category>/<dashboard-name>.json`. <br>
Grafana will automatically sync with `dashboards/` and **update**/**create** when it detect changes.

## 📄 Create a new Dashboard
> While we could create new Dashboard directly from the UI, generating them from a file directly let us manage UIDs avoiding long unreadable ones -> shorter urls and better data links visibility.

To create a new dashboard add a **JSON** file with implicit name in the corresponding folder.
- The `uid` has to be unique.
- While you can have similar title in different folders, to avoid any future problems, it's best to make the `title` also unique.
```json
// dashboards/monitoring/app-ressources.json

{
	"title": "App - Ressources",
	"uid": "app-monitoring-ressources"
}
``` 
Grafana will generate the dashboard within few seconds.
## 📝 Modify a Dashboard
Select the dashboard you want to change in the UI, do some changes then:
1. Exit edit mode.
2. In the top-right corner: **Export** -> **Export as JSON**.
3. Copy past the content into the corresponding **JSON** file.
4. Make sure that all **datasources** are using a provisioned one.
	```json
	// ❌ This could cause issues with migration
	"datasource": {
		"type": "grafana-postgresql-datasource",
		"uid": "P44368ADAD746BC27"
	}

	// ✅ No problem, this is a provisioned datasource
	"datasource": {
	     "type": "grafana-postgresql-datasource",
	     "uid": "Postgres"
	}
	```
	You can check existing provisioned data sources in [datasources.yaml](../grafana/provisioning/datasources/datasources.yaml)
5. Save and commit your changes.
