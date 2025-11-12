import React, { useState } from 'react';
import { Layout } from '../components/Layout';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { agentsAPI } from '../services/api';

const AgentCreate: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    system_prompt: '',
    greeting_message: '',
    voice_id: '21m00Tcm4TlvDq8ikWAM',
    voice_provider: 'elevenlabs',
    language: 'de',
  });

  const createMutation = useMutation({
    mutationFn: (data: any) => agentsAPI.create(data),
    onSuccess: () => {
      navigate('/agents');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate(formData);
  };

  return (
    <Layout>
      <div className="max-w-3xl">
        <h1 className="text-3xl font-bold text-gray-900">Create New Agent</h1>

        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">Agent Name</label>
            <input
              type="text"
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">System Prompt</label>
            <textarea
              required
              rows={4}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              placeholder="Du bist ein freundlicher Kundenservice-Agent..."
              value={formData.system_prompt}
              onChange={(e) => setFormData({ ...formData, system_prompt: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Greeting Message</label>
            <input
              type="text"
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              placeholder="Guten Tag! Wie kann ich Ihnen helfen?"
              value={formData.greeting_message}
              onChange={(e) => setFormData({ ...formData, greeting_message: e.target.value })}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Language</label>
              <select
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                value={formData.language}
                onChange={(e) => setFormData({ ...formData, language: e.target.value })}
              >
                <option value="de">German (de)</option>
                <option value="en">English (en)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Voice Provider</label>
              <select
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                value={formData.voice_provider}
                onChange={(e) => setFormData({ ...formData, voice_provider: e.target.value })}
              >
                <option value="elevenlabs">ElevenLabs</option>
              </select>
            </div>
          </div>

          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={() => navigate('/agents')}
              className="rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={createMutation.isPending}
              className="rounded-md border border-transparent bg-primary-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50"
            >
              {createMutation.isPending ? 'Creating...' : 'Create Agent'}
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
};

export default AgentCreate;
