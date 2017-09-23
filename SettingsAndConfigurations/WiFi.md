# Connecting to University of Utah WiFi
-----------

In `/etc/wpa_supplicant/wpa_supplicant.conf`, add the following entry. Replace `<UID>` and `<PASSWORD>` with correct credentials.

```
network={
	ssid="UConnect"
	key_mgmt=WPA-EAP
	eap=PEAP
	identity="<UID>"
	password="<PASSWORD>"
	phase1="peaplabel=auto tls_disable_tlsv1_2=1"
	phase2="auth=MSCHAPV2"
}
```

## Troubleshooting
- If it doesn't automatically detect changes: `sudo wpa_cli reconfigure`
- Verify connection: `ifconfig`
