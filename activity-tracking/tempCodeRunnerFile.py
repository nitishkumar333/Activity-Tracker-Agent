    """Check for local screenshots and upload them to S3."""
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                directory = os.path.join(script_dir, "Queue", "Screen_Shot")
                
                if os.path.exists(directory):
                    files = os.listdir(directory)
                    for Local in files:
                        Inet = self.check_internet_connection()
                        if Inet:
                            file_path = os.path.join(directory, Local)
                            if os.path.isfile(file_path):
                                try:
                                    # Check if the file is a screenshot (e.g., ends with .png or .jpg)
                                    if Local.lower().endswith(('.png', '.jpg', '.jpeg')):
                                        # Open the image file to upload
                                        with Image.open(file_path) as image:
                                            # Upload the screenshot to S3
                                            self.upload_SS_to_s3(image,self.file_name_ss,Local)  # Use the correct upload function
                                            print(f"Uploaded screenshot {Local} to S3.")
                                        
                                        # Delete the file after successful upload
                                        os.remove(file_path)
                                        print(f"Deleted local screenshot file: {Local}")
                                except Exception as e:
                                    print(f"Error uploading {Local} to S3: {str(e)}")
            except Exception as e:
                print(f"Error checking local screenshots for upload: {str(e)}")