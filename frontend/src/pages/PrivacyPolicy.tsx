import React from 'react';

const PrivacyPolicy: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-lg shadow">
        <h1 className="text-3xl font-bold text-gray-900">Datenschutzerklärung (Privacy Policy)</h1>
        <div className="mt-6 prose">
          <p>Diese Datenschutzerklärung informiert Sie über die Verarbeitung Ihrer personenbezogenen Daten.</p>
          <h2>1. Verantwortlicher</h2>
          <p>CAL - AI Phone Agent Assistant System</p>
          <h2>2. Erhobene Daten</h2>
          <ul>
            <li>E-Mail-Adresse und Passwort (verschlüsselt)</li>
            <li>AI-Agent-Konfigurationen</li>
            <li>Telefonaufzeichnungen und Transkripte</li>
            <li>Anrufmetadaten</li>
          </ul>
          <h2>3. Rechtsgrundlage</h2>
          <p>Die Verarbeitung erfolgt auf Basis Ihrer ausdrücklichen Einwilligung (DSGVO Art. 6 Abs. 1 lit. a).</p>
          <h2>4. Datenspeicherung</h2>
          <ul>
            <li>Anrufaufzeichnungen: 90 Tage</li>
            <li>Transkripte: 180 Tage, danach anonymisiert</li>
            <li>Kontodaten: Bis zur Löschung des Kontos</li>
          </ul>
          <h2>5. Ihre Rechte</h2>
          <ul>
            <li>Recht auf Auskunft</li>
            <li>Recht auf Berichtigung</li>
            <li>Recht auf Löschung</li>
            <li>Recht auf Datenübertragbarkeit</li>
            <li>Recht auf Widerruf der Einwilligung</li>
          </ul>
          <h2>6. Datensicherheit</h2>
          <p>Alle Daten werden verschlüsselt gespeichert und übertragen.</p>
        </div>
      </div>
    </div>
  );
};

export default PrivacyPolicy;
