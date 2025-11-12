import React from 'react';

const TermsOfService: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-lg shadow">
        <h1 className="text-3xl font-bold text-gray-900">Nutzungsbedingungen (Terms of Service)</h1>
        <div className="mt-6 prose">
          <h2>1. Akzeptanz der Bedingungen</h2>
          <p>Durch die Nutzung von CAL akzeptieren Sie diese Nutzungsbedingungen.</p>
          <h2>2. Leistungsbeschreibung</h2>
          <p>CAL bietet AI-gestützte Telefonagenten-Dienste.</p>
          <h2>3. Nutzerverantwortlichkeiten</h2>
          <ul>
            <li>Sicherheit des Kontos gewährleisten</li>
            <li>Einhaltung geltender Gesetze</li>
            <li>Einholung von Einwilligungen vor Aufzeichnung von Anrufen</li>
          </ul>
          <h2>4. Datenverarbeitung</h2>
          <p>Sie stimmen der Datenverarbeitung gemäß unserer Datenschutzerklärung zu.</p>
          <h2>5. Kündigung</h2>
          <p>Sie können Ihr Konto jederzeit kündigen.</p>
          <h2>6. Haftungsbeschränkung</h2>
          <p>Der Dienst wird "wie besehen" ohne Gewährleistung bereitgestellt.</p>
        </div>
      </div>
    </div>
  );
};

export default TermsOfService;
