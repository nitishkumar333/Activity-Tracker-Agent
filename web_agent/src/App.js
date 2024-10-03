import React, { useEffect, useState } from "react";
import s3 from "./awsConfig.js";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    interval: 10,
    screenshot: false,
    blur: false,
  });

  const getFileFromS3 = async () => {
    const params = {
      Bucket: process.env.REACT_APP_AWS_BUCKET_NAME,
      Key: "python_agent_data.json",
    };

    try {
      const data = await s3.getObject(params).promise();
      const fileContent = JSON.parse(data.Body.toString("utf-8"));
      setFormData({
        interval: fileContent.interval,
        screenshot: fileContent.screenshot,
        blur: fileContent.blur,
      });
      console.log(fileContent);
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

    if (name === "interval" && value < 10) {
      alert("Interval must be greater than or equal to 10");
      return;
    }

    if (name === "screenshot" && !checked) {
      setFormData({
        ...formData,
        screenshot: checked,
        interval: 10,
        blur: false,
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
    await uploadToS3(formData);
  };

  return (
    <div className="App">
      <h2>Web Agent</h2>
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

        <div className="form-group">
          <label>Interval in sec(min 10):</label>
          <input
            type="number"
            name="interval"
            min={10}
            value={formData.interval}
            onChange={handleChange}
            required
            disabled={!formData.screenshot}
          />
        </div>

        <div className="form-group">
          <label>Blur On/Off:</label>
          <input
            type="checkbox"
            name="blur"
            checked={formData.blur}
            onChange={handleChange}
            disabled={!formData.screenshot}
          />
        </div>

        <button type="submit">Save</button>
      </form>
    </div>
  );
}

export default App;
