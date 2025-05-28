import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    company: '',
    jobDescription: '',
    senderEmail: '',
    senderPassword: ''
  });
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [credentialsStatus, setCredentialsStatus] = useState(null);
  const [validationErrors, setValidationErrors] = useState({});
  const [hasSubmitted, setHasSubmitted] = useState(false);
  const [showCredentialFields, setShowCredentialFields] = useState(false);

  // Check credentials status on component mount
  React.useEffect(() => {
    checkCredentialsStatus();
  }, []);

  const checkCredentialsStatus = async () => {
    try {
      const response = await axios.get('http://localhost:5001/credentials-status');
      setCredentialsStatus(response.data);
    } catch (err) {
      console.log('Could not check credentials status');
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const validateForm = () => {
    const errors = {};
    
    if (!formData.firstName.trim()) errors.firstName = 'First name is required';
    if (!formData.lastName.trim()) errors.lastName = 'Last name is required';
    if (!formData.company.trim()) errors.company = 'Company is required';
    if (!formData.jobDescription.trim()) errors.jobDescription = 'Job description is required';
    
    // Only validate email fields if credentials are not stored AND no override credentials provided
    const needsCredentials = !credentialsStatus?.has_credentials;
    const providingOverride = showCredentialFields && (formData.senderEmail.trim() || formData.senderPassword.trim());
    
    if (needsCredentials || (showCredentialFields && !credentialsStatus?.has_credentials)) {
      if (!formData.senderEmail.trim()) errors.senderEmail = 'Email is required';
      if (!formData.senderPassword.trim()) errors.senderPassword = 'Password is required';
    }
    
    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setHasSubmitted(true);
    
    const errors = validateForm();
    setValidationErrors(errors);
    
    if (Object.keys(errors).length > 0) {
      return; // Don't submit if there are validation errors
    }
    
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:5001/send-email', formData);
      setResult(response.data);
      setHasSubmitted(false); // Reset validation state on success
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred while sending emails');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      firstName: '',
      lastName: '',
      company: '',
      jobDescription: '',
      senderEmail: '',
      senderPassword: ''
    });
    setResult(null);
    setError(null);
    setValidationErrors({});
    setHasSubmitted(false);
  };

  return (
    <div className="App">
      {/* Professional Banner */}
      <div className="banner">
        <div className="banner-content">
          <div className="banner-left">
            <h2>🚀 Cold Email Automation Platform</h2>
            <p>Intelligent job referral emails with AI-powered template selection</p>
          </div>
          <div className="banner-right">
            <div className="stats">
              <div className="stat-item">
                <span className="stat-number">3</span>
                <span className="stat-label">Templates</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">8</span>
                <span className="stat-label">Email Patterns</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">100%</span>
                <span className="stat-label">Automated</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container">
        <h1>Send Cold Email</h1>
        <p className="subtitle">Personalized job referral emails with automatic template selection</p>
        
        {credentialsStatus && (
          <div className={`credentials-status ${credentialsStatus.has_credentials ? 'success' : 'warning'}`}>
            {credentialsStatus.has_credentials ? (
              <div>
                <p>✅ <strong>Credentials stored and ready!</strong></p>
                <p>📧 Email: {credentialsStatus.email} (via {credentialsStatus.source})</p>
                <p>🎯 You can send emails directly without entering credentials again!</p>
                {!showCredentialFields && (
                  <button 
                    type="button" 
                    className="override-btn"
                    onClick={() => setShowCredentialFields(true)}
                  >
                    Use Different Credentials
                  </button>
                )}
                {showCredentialFields && (
                  <button 
                    type="button" 
                    className="override-btn secondary"
                    onClick={() => setShowCredentialFields(false)}
                  >
                    Use Stored Credentials
                  </button>
                )}
              </div>
            ) : (
              <p>⚠️ <strong>No stored credentials found.</strong> You'll need to enter your email and password below, or run the setup script.</p>
            )}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="email-form">
          <div className="form-group">
            <label htmlFor="firstName">First Name *</label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              value={formData.firstName}
              onChange={handleChange}
              className={hasSubmitted && validationErrors.firstName ? 'error' : ''}
              placeholder="Enter recipient's first name"
            />
            {hasSubmitted && validationErrors.firstName && (
              <span className="error-text">{validationErrors.firstName}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="lastName">Last Name *</label>
            <input
              type="text"
              id="lastName"
              name="lastName"
              value={formData.lastName}
              onChange={handleChange}
              className={hasSubmitted && validationErrors.lastName ? 'error' : ''}
              placeholder="Enter recipient's last name"
            />
            {hasSubmitted && validationErrors.lastName && (
              <span className="error-text">{validationErrors.lastName}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="company">Company *</label>
            <input
              type="text"
              id="company"
              name="company"
              value={formData.company}
              onChange={handleChange}
              className={hasSubmitted && validationErrors.company ? 'error' : ''}
              placeholder="Enter company name"
            />
            {hasSubmitted && validationErrors.company && (
              <span className="error-text">{validationErrors.company}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="jobDescription">Job Description *</label>
            <input
              type="text"
              id="jobDescription"
              name="jobDescription"
              value={formData.jobDescription}
              onChange={handleChange}
              className={hasSubmitted && validationErrors.jobDescription ? 'error' : ''}
              placeholder="e.g., Software Engineer, Data Scientist, Business Analyst"
            />
            {hasSubmitted && validationErrors.jobDescription && (
              <span className="error-text">{validationErrors.jobDescription}</span>
            )}
          </div>

          {(!credentialsStatus?.has_credentials || showCredentialFields) && (
            <>
              <div className="form-group">
                <label htmlFor="senderEmail">Your Email {!credentialsStatus?.has_credentials ? '*' : '(Optional - Override)'}</label>
                <input
                  type="email"
                  id="senderEmail"
                  name="senderEmail"
                  value={formData.senderEmail}
                  onChange={handleChange}
                  className={hasSubmitted && validationErrors.senderEmail ? 'error' : ''}
                  placeholder="your.email@gmail.com"
                />
                {hasSubmitted && validationErrors.senderEmail && (
                  <span className="error-text">{validationErrors.senderEmail}</span>
                )}
              </div>

              <div className="form-group">
                <label htmlFor="senderPassword">Email Password/App Password {!credentialsStatus?.has_credentials ? '*' : '(Optional - Override)'}</label>
                <input
                  type="password"
                  id="senderPassword"
                  name="senderPassword"
                  value={formData.senderPassword}
                  onChange={handleChange}
                  className={hasSubmitted && validationErrors.senderPassword ? 'error' : ''}
                  placeholder="Your email password or app password"
                />
                {hasSubmitted && validationErrors.senderPassword && (
                  <span className="error-text">{validationErrors.senderPassword}</span>
                )}
                <small className="help-text">
                  For Gmail, use an App Password instead of your regular password
                </small>
              </div>
            </>
          )}

          <div className="form-actions">
            <button type="submit" disabled={loading} className="submit-btn">
              {loading ? 'Sending Emails...' : 'Send Emails'}
            </button>
            <button type="button" onClick={resetForm} className="reset-btn">
              Reset Form
            </button>
          </div>
        </form>

        {error && (
          <div className="error-message">
            <h3>Error</h3>
            <p>{error}</p>
          </div>
        )}

        {result && (
          <div className="success-message">
            <h3>Success!</h3>
            <p>{result.message}</p>
            <div className="result-details">
              <p><strong>Job Type Detected:</strong> {result.job_type}</p>
              <p><strong>Emails Sent To:</strong></p>
              <ul>
                {result.sent_emails.map((email, index) => (
                  <li key={index}>{email}</li>
                ))}
              </ul>
              {result.failed_emails.length > 0 && (
                <div>
                  <p><strong>Failed Emails:</strong></p>
                  <ul>
                    {result.failed_emails.map((failed, index) => (
                      <li key={index}>{failed.email} - {failed.error}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}

        <div className="info-section">
          <h3>🔧 How it works:</h3>
          <div className="info-grid">
            <div className="info-item">
              <div className="info-icon">📝</div>
              <div className="info-content">
                <h4>Enter Details</h4>
                <p>Provide recipient's name, company, and job description</p>
              </div>
            </div>
            <div className="info-item">
              <div className="info-icon">🤖</div>
              <div className="info-content">
                <h4>AI Detection</h4>
                <p>Automatically detects job type (Engineer/Analyst/ML)</p>
              </div>
            </div>
            <div className="info-item">
              <div className="info-icon">📧</div>
              <div className="info-content">
                <h4>Smart Templates</h4>
                <p>Selects appropriate email template and resume</p>
              </div>
            </div>
            <div className="info-item">
              <div className="info-icon">🎯</div>
              <div className="info-content">
                <h4>Multi-Send</h4>
                <p>Generates 8 email patterns and sends to all</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 