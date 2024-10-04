import React, { useEffect, useState } from "react";
import s3 from "../awsConfig.js";
import "./config.css";
import { auth } from "./firebase";

function Config() {
  const [formData, setFormData] = useState({
    interval: 10, // Default interval
    screenshot: false, // Default screenshot unchecked
    blur: false, // Default blur unchecked
  });

  const getFileFromS3 = async () => {
    const params = {
      Bucket: process.env.REACT_APP_AWS_BUCKET_NAME,
      Key: "python_agent_data.json", // The file's name in S3
    };

    try {
      // Fetch the file from S3
      const data = await s3.getObject(params).promise();

      // Convert the JSON file content to a JavaScript object
      const fileContent = JSON.parse(data.Body.toString("utf-8"));
      setFormData({
        interval: fileContent.interval,
        screenshot: fileContent.screenshot,
        blur: fileContent.blur,
      });
      console.log(fileContent); // The JSON data as a JavaScript object
      return fileContent;
    } catch (error) {
      console.error("Error fetching file from S3:", error);
    }
  };

  useEffect(() => {
    getFileFromS3();
  }, []);

  const BUCKET_NAME = process.env.REACT_APP_AWS_BUCKET_NAME;

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    // Special handling for screenshot checkbox
    if (name === "screenshot" && !checked) {
      // If screenshot is unchecked, reset interval and blur
      setFormData({
        ...formData,
        screenshot: checked,
        interval: 10, // Reset interval to default value
        blur: false, // Reset blur
      });
    } else {
      setFormData({
        ...formData,
        [name]: type === "checkbox" ? checked : value,
      });
    }
  };

  const uploadToS3 = async (data) => {
    const fileName = "python_agent_data.json";

    const params = {
      Bucket: BUCKET_NAME,
      Key: fileName,
      Body: JSON.stringify(data),
      ContentType: "application/json",
    };

    try {
      await s3.upload(params).promise();
      alert("File uploaded successfully");
    } catch (error) {
      alert("Error uploading file to S3");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.interval < 10) {
      // Ensure interval is at least 10
      alert("Interval must be greater than or equal to 10");
      return;
    }
    await uploadToS3(formData);
  };

  async function handleLogout() {
    try {
      await auth.signOut();
      window.location.href = "/login";
      console.log("User logged out successfully!");
    } catch (error) {
      console.error("Error logging out:", error.message);
    }
  }

  return (
    <div className="Config">
      <h2 className="heading">CONFIGURATIONS</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Screenshot On/Off:</label>
          <input
            type="checkbox"
            name="screenshot"
            checked={formData.screenshot}
            onChange={handleChange}
          />
        </div>

        <div className="form-group-num">
          <label>Interval in sec(min 10):</label>
          <input
            type="number"
            name="interval"
            min={10}
            value={formData.interval}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Blur On/Off:</label>
          <input
            type="checkbox"
            name="blur"
            checked={formData.blur}
            onChange={handleChange}
            disabled={!formData.screenshot} // Disable if screenshot is not checked
          />
        </div>
        <div className="btns">
          <button type="submit" className="btn1">SAVE</button>
          <button className="logoutBtn" onClick={handleLogout} type="button">LOGOUT</button>
        </div>
      </form>
    </div>
  );
}

export default Config;
