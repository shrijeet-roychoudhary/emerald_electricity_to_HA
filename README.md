# Emerald Electricity to Home Assistant

This is a custom integration for Home Assistant that allows you to monitor your electricity usage from your Emerald Energy monitor.

## Installation

There are two ways to install this integration:

### Manual Installation (Recommended for now)

1.  **Download the integration files:**
    *   Click [here](https://github.com/shrijeet-roychoudhary/emerald_electricity_to_HA/archive/refs/heads/main.zip) to download the integration files as a zip file.
    *   Unzip the downloaded file. You will find a folder named `emerald_electricity_to_HA-main`.

2.  **Find your Home Assistant `custom_components` folder:**
    *   This folder is usually located in the same directory as your `configuration.yaml` file.
    *   If you are using Home Assistant OS, you can find it by using the "Samba" or "SSH" add-on.
    *   If you are using Home Assistant Core, it's in the root of your configuration directory.

3.  **Copy the integration files:**
    *   Inside the `emerald_electricity_to_HA-main` folder, you will find a folder named `emerald_to_ha`.
    *   Inside `emerald_to_ha`, there is a folder named `emerald_energy`.
    *   Copy the `emerald_energy` folder into your `custom_components` folder in Home Assistant.

    Your folder structure should look like this:
    ```
    <config>/
    |-- custom_components/
    |   |-- emerald_energy/
    |       |-- __init__.py
    |       |-- sensor.py
    |       |-- ...
    ```

4.  **Restart Home Assistant:**
    *   This is a very important step! Restart your Home Assistant instance to make it recognize the new integration.
    *   You can do this by going to **Settings > System > Restart**.

### Installation via HACS (Home Assistant Community Store)

*At the moment, this integration is not available in HACS. We are working on it!* 

## Configuration

Once the integration is installed and Home Assistant is restarted, you can add it to your Home Assistant configuration.

1.  **Go to Devices & Services:**
    *   In the Home Assistant UI, go to **Settings > Devices & Services**.

2.  **Add the integration:**
    *   Click the **+ ADD INTEGRATION** button in the bottom right corner.
    *   Search for "Emerald Energy".
    *   Click on the "Emerald Energy" integration.

3.  **Enter your credentials:**
    *   A dialog box will appear asking for your Emerald Energy email and password.
    *   Enter your credentials and click **Submit**.

4.  **Done!**
    *   If your credentials are correct, the integration will be added and you will see a confirmation message.

## Finding your new sensor

The integration will create a sensor named `sensor.emerald_energy`. You can add this sensor to your dashboard to see your daily electricity consumption.

1.  **Go to your dashboard.**
2.  **Click the three dots in the top right corner and select "Edit Dashboard".**
3.  **Click the "+ ADD CARD" button.**
4.  **Search for the "Sensor" card.**
5.  **In the "Entity" field, search for `sensor.emerald_energy`.**
6.  **Click "Save".**

You should now see your daily electricity consumption on your dashboard!

## Troubleshooting

*   **I can't find the integration in the "Add Integration" list:**
    *   Make sure you have copied the `emerald_energy` folder (and not `emerald_to_ha` or `emerald_electricity_to_HA-main`) into the `custom_components` folder.
    *   Make sure you have restarted Home Assistant after copying the files.

*   **I get an "invalid_auth" error when I enter my credentials:**
    *   Double-check your email and password.
    *   Make sure you can log in to the Emerald Energy website with the same credentials.

*   **The sensor shows "unknown" or "unavailable":**
    *   This can happen if the integration is having trouble connecting to the Emerald API.
    *   Please check your internet connection.
    *   You can check the Home Assistant logs for more detailed error messages. Go to **Settings > System > Logs**.

If you are still having issues, please [open an issue on GitHub](https://github.com/shrijeet-roychoudhary/emerald_electricity_to_HA/issues).
