import React from 'react';
import { Layout } from '../components/Layout';
import { gdprAPI } from '../services/api';

const Settings: React.FC = () => {
  const handleExportData = async () => {
    const response = await gdprAPI.exportData();
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `user_data_${Date.now()}.json`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  return (
    <Layout>
      <h1 className="text-3xl font-bold text-gray-900">Settings</h1>

      <div className="mt-8 space-y-6">
        <div className="bg-white shadow sm:rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium leading-6 text-gray-900">Export Your Data</h3>
            <div className="mt-2 max-w-xl text-sm text-gray-500">
              <p>Download all your data in JSON format (GDPR Right to Access)</p>
            </div>
            <div className="mt-5">
              <button
                onClick={handleExportData}
                className="inline-flex items-center justify-center rounded-md border border-transparent bg-primary-600 px-4 py-2 font-medium text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 sm:text-sm"
              >
                Export Data
              </button>
            </div>
          </div>
        </div>

        <div className="bg-white shadow sm:rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium leading-6 text-gray-900">Delete Account</h3>
            <div className="mt-2 max-w-xl text-sm text-gray-500">
              <p>Permanently delete your account and all data (GDPR Right to Erasure)</p>
            </div>
            <div className="mt-5">
              <button
                onClick={() => alert('Delete account functionality - implement confirmation flow')}
                className="inline-flex items-center justify-center rounded-md border border-transparent bg-red-600 px-4 py-2 font-medium text-white shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 sm:text-sm"
              >
                Delete Account
              </button>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Settings;
