import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

export default function NotFound() {
  return (
    <Layout title="Page Not Found">
      <div className="container margin-vert--xl">
        <div className="row">
          <div className="col">
            <h1>Page Not Found</h1>
            <p>The page you are looking for does not exist.</p>
            <Link to="/docs/001-project-setup">Go to Chapter 1</Link>
          </div>
        </div>
      </div>
    </Layout>
  );
}
