while not stop[0]:
            battery = psutil.sensors_battery()  # Get battery status
            if battery is not None:
                self.percentage = battery.percent
                self.is_plugged = [battery.power_plugged]