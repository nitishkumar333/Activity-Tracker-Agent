import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    name: '',
    number: '',
    toggle: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
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
