import React, { useState } from 'react';
import AWS from 'aws-sdk';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    name: '',
    number: '',
    toggle: false,
  });

  // AWS S3 Configuration
  AWS.config.update({
    accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY,
    region: process.env.REACT_APP_AWS_REGION_NAME,
  });

  const s3 = new AWS.S3();
  const BUCKET_NAME = process.env.REACT_APP_AWS_BUCKET_NAME;

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };
  
  const uploadToS3 = async (data) => {
    const fileName = `python_agent_data.json`;

    const params = {
      Bucket: BUCKET_NAME,
      Key: fileName,
      Body: JSON.stringify(data),
      ContentType: 'application/json',
    };

    try {
      await s3.upload(params).promise();
      alert(`File uploaded successfully`);
    } catch (error) {
      alert('Error uploading file to S3');
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
          <label>Name:</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Number:</label>
          <input
            type="number"
            name="number"
            value={formData.number}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Toggle On/Off:</label>
          <input
            type="checkbox"
            name="toggle"
            checked={formData.toggle}
            onChange={handleChange}
          />
        </div>

        <button type="submit">Save & Upload</button>
      </form>
    </div>
  );
}

export default App;
