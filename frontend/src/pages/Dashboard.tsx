import React from 'react';
import { Layout } from '../components/Layout';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { agentsAPI, callsAPI } from '../services/api';

const Dashboard: React.FC = () => {
  const { data: agents } = useQuery({
    queryKey: ['agents'],
    queryFn: () => agentsAPI.list().then(res => res.data),
  });

  const { data: conversations } = useQuery({
    queryKey: ['conversations'],
    queryFn: () => callsAPI.listConversations({ limit: 5 }).then(res => res.data),
  });

  return (
    <Layout>
      <div className="px-4 sm:px-0">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-sm text-gray-700">
          Übersicht über Ihre AI Phone Agents
        </p>
      </div>

      <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {/* Stats */}
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-500 truncate">Agents</p>
                <p className="mt-1 text-3xl font-semibold text-gray-900">{agents?.length || 0}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-500 truncate">Recent Calls</p>
                <p className="mt-1 text-3xl font-semibold text-gray-900">{conversations?.length || 0}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-8">
        <h2 className="text-lg font-medium text-gray-900">Quick Actions</h2>
        <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <Link
            to="/agents/new"
            className="relative block w-full bg-white border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-primary-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <span className="mt-2 block text-sm font-medium text-gray-900">Create New Agent</span>
          </Link>
          <Link
            to="/agents"
            className="relative block w-full bg-white border-2 border-gray-300 rounded-lg p-6 text-center hover:border-primary-400"
          >
            <span className="mt-2 block text-sm font-medium text-gray-900">View All Agents</span>
          </Link>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;
