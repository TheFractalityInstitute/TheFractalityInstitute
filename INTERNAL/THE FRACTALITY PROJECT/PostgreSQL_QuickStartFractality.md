
``` bash
#!/bin/bash
# Fractality PostgreSQL Quick Start Script
# Run this to get PostgreSQL up and running TODAY!

echo "🚀 Fractality PostgreSQL Setup"
echo "=============================="

# Step 1: Install PostgreSQL (uncomment for your OS)
echo "📦 Step 1: Installing PostgreSQL..."

# macOS
# brew install postgresql@15
# brew services start postgresql@15

# Ubuntu/Debian
# sudo apt update
# sudo apt install postgresql postgresql-contrib

# Windows
# Download installer from https://www.postgresql.org/download/windows/

# Step 2: Create database and user
echo "🏗️ Step 2: Creating Fractality database..."

# Create the database
sudo -u postgres psql << EOF
-- Create user (change password!)
CREATE USER fractality WITH PASSWORD 'cosmic_consciousness_2025';

-- Create database
CREATE DATABASE fractality_db OWNER fractality;

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE fractality_db TO fractality;

-- Connect to the new database
\c fractality_db

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create initial schema
CREATE SCHEMA consciousness;
GRANT ALL ON SCHEMA consciousness TO fractality;

-- Set search path
ALTER DATABASE fractality_db SET search_path TO consciousness, public;
EOF

# Step 3: Create initial tables
echo "📊 Step 3: Creating initial tables..."

PGPASSWORD='cosmic_consciousness_2025' psql -U fractality -d fractality_db << 'EOF'
-- Switch to consciousness schema
SET search_path TO consciousness, public;

-- Core nodes table
CREATE TABLE nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_key VARCHAR(255) UNIQUE NOT NULL,
    label TEXT,
    type VARCHAR(50) DEFAULT 'concept',
    depth INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    energy JSONB DEFAULT '{"ATP": 1.0, "network": "default", "efficiency": 1.0}',
    resonance JSONB DEFAULT '{"semanticScore": 0.0, "tfidfScore": 0.0}',
    visual JSONB DEFAULT '{"position": {"x": 0, "y": 0, "z": 0}, "scale": 1.0, "color": "#00ff00"}',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255) DEFAULT 'system'
);

-- Edges for relationships
CREATE TABLE edges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_node_id UUID NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
    to_node_id UUID NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) DEFAULT 'child',
    weight FLOAT DEFAULT 1.0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(from_node_id, to_node_id, relationship_type)
);

-- Consciousness streams (time-series data)
CREATE TABLE consciousness_streams (
    id UUID DEFAULT uuid_generate_v4(),
    node_id UUID NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atp_level FLOAT NOT NULL,
    attention_score FLOAT DEFAULT 0.0,
    resonance_vector FLOAT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    PRIMARY KEY (node_id, timestamp)
);

-- Create indexes for performance
CREATE INDEX idx_nodes_key ON nodes(node_key);
CREATE INDEX idx_nodes_type ON nodes(type);
CREATE INDEX idx_nodes_metadata_gin ON nodes USING GIN (metadata);
CREATE INDEX idx_nodes_energy_atp ON nodes ((energy->>'ATP'));
CREATE INDEX idx_edges_from ON edges(from_node_id);
CREATE INDEX idx_edges_to ON edges(to_node_id);
CREATE INDEX idx_consciousness_timestamp ON consciousness_streams(timestamp DESC);

-- Create update trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_nodes_updated_at
BEFORE UPDATE ON nodes
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- Insert some initial test data
INSERT INTO nodes (node_key, label, type, metadata) VALUES
('fractality-root', 'Fractality Root', 'root', '{"description": "The origin of all consciousness"}'),
('quantum-consciousness', 'Quantum Consciousness', 'concept', '{"tags": ["quantum", "consciousness"]}'),
('collective-mind', 'Collective Mind', 'concept', '{"tags": ["collective", "emergence"]}'),
('individual-thought', 'Individual Thought', 'concept', '{"tags": ["personal", "thought"]}');

-- Create some relationships
INSERT INTO edges (from_node_id, to_node_id, relationship_type) VALUES
((SELECT id FROM nodes WHERE node_key = 'fractality-root'), 
 (SELECT id FROM nodes WHERE node_key = 'quantum-consciousness'), 'child'),
((SELECT id FROM nodes WHERE node_key = 'fractality-root'), 
 (SELECT id FROM nodes WHERE node_key = 'collective-mind'), 'child'),
((SELECT id FROM nodes WHERE node_key = 'collective-mind'), 
 (SELECT id FROM nodes WHERE node_key = 'individual-thought'), 'child');

-- Verify installation
SELECT 'Installation complete!' as message;
SELECT COUNT(*) as node_count FROM nodes;
SELECT COUNT(*) as edge_count FROM edges;
EOF

# Step 4: Create Node.js connection file
echo "📝 Step 4: Creating Node.js connection file..."

cat > db-config.js << 'EOF'
// db-config.js - PostgreSQL connection configuration
import pkg from 'pg';
const { Pool } = pkg;

// Connection configuration
const config = {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME || 'fractality_db',
    user: process.env.DB_USER || 'fractality',
    password: process.env.DB_PASSWORD || 'cosmic_consciousness_2025',
    
    // Pool configuration
    max: 20,                    // Maximum connections
    idleTimeoutMillis: 30000,   // Close idle connections after 30s
    connectionTimeoutMillis: 2000, // Timeout after 2s
};

// Create connection pool
export const pool = new Pool(config);

// Error handling
pool.on('error', (err, client) => {
    console.error('Unexpected error on idle client', err);
    process.exit(-1);
});

// Test connection
export async function testConnection() {
    try {
        const client = await pool.connect();
        const result = await client.query('SELECT NOW()');
        console.log('✅ PostgreSQL connected:', result.rows[0].now);
        client.release();
        return true;
    } catch (err) {
        console.error('❌ PostgreSQL connection error:', err);
        return false;
    }
}

// Helper functions
export async function query(text, params) {
    const start = Date.now();
    const res = await pool.query(text, params);
    const duration = Date.now() - start;
    
    // Log slow queries
    if (duration > 100) {
        console.log('executed query', { text, duration, rows: res.rowCount });
    }
    
    return res;
}

export async function getClient() {
    const client = await pool.connect();
    const query = client.query;
    const release = client.release;
    
    // Set a timeout of 5 seconds, after which we will log this client's last query
    const timeout = setTimeout(() => {
        console.error('A client has been checked out for more than 5 seconds!');
        console.error(`The last executed query on this client was: ${client.lastQuery}`);
    }, 5000);
    
    // Monkey patch the query method to keep track of the last query executed
    client.query = (...args) => {
        client.lastQuery = args;
        return query.apply(client, args);
    };
    
    client.release = () => {
        clearTimeout(timeout);
        client.query = query;
        client.release = release;
        return release.apply(client);
    };
    
    return client;
}

// Transaction helper
export async function transaction(callback) {
    const client = await getClient();
    try {
        await client.query('BEGIN');
        const result = await callback(client);
        await client.query('COMMIT');
        return result;
    } catch (e) {
        await client.query('ROLLBACK');
        throw e;
    } finally {
        client.release();
    }
}

// Cleanup on exit
process.on('beforeExit', async () => {
    await pool.end();
});
EOF

# Step 5: Create test script
echo "🧪 Step 5: Creating test script..."

cat > test-db.js << 'EOF'
// test-db.js - Test your PostgreSQL connection
import { testConnection, query, transaction } from './db-config.js';

async function runTests() {
    console.log('🧪 Testing Fractality PostgreSQL Setup\n');
    
    // Test 1: Connection
    console.log('Test 1: Basic connection');
    const connected = await testConnection();
    if (!connected) {
        console.error('Failed to connect to PostgreSQL!');
        process.exit(1);
    }
    
    // Test 2: Query nodes
    console.log('\nTest 2: Querying nodes');
    const nodes = await query('SELECT * FROM consciousness.nodes ORDER BY created_at');
    console.log(`Found ${nodes.rows.length} nodes:`);
    nodes.rows.forEach(node => {
        console.log(`  - ${node.node_key}: ${node.label}`);
    });
    
    // Test 3: Create a new node
    console.log('\nTest 3: Creating a new node');
    const newNode = await query(
        `INSERT INTO consciousness.nodes (node_key, label, metadata) 
         VALUES ($1, $2, $3) 
         RETURNING *`,
        ['test-node-' + Date.now(), 'Test Node', { tags: ['test'], timestamp: new Date() }]
    );
    console.log('Created node:', newNode.rows[0].node_key);
    
    // Test 4: Transaction test
    console.log('\nTest 4: Transaction test');
    try {
        await transaction(async (client) => {
            // Create parent
            const parent = await client.query(
                `INSERT INTO consciousness.nodes (node_key, label) 
                 VALUES ($1, $2) RETURNING id`,
                ['transaction-parent', 'Transaction Parent']
            );
            
            // Create child
            const child = await client.query(
                `INSERT INTO consciousness.nodes (node_key, label) 
                 VALUES ($1, $2) RETURNING id`,
                ['transaction-child', 'Transaction Child']
            );
            
            // Create edge
            await client.query(
                `INSERT INTO consciousness.edges (from_node_id, to_node_id) 
                 VALUES ($1, $2)`,
                [parent.rows[0].id, child.rows[0].id]
            );
            
            console.log('Transaction completed successfully!');
        });
    } catch (error) {
        console.error('Transaction failed:', error.message);
    }
    
    // Test 5: JSON operations
    console.log('\nTest 5: JSONB operations');
    const jsonTest = await query(`
        UPDATE consciousness.nodes 
        SET 
            energy = jsonb_set(energy, '{ATP}', '0.95'),
            metadata = metadata || '{"lastTest": "successful"}'
        WHERE node_key = $1
        RETURNING node_key, energy, metadata
    `, ['quantum-consciousness']);
    
    if (jsonTest.rows.length > 0) {
        console.log('Updated node energy:', jsonTest.rows[0].energy);
    }
    
    console.log('\n✅ All tests completed!');
    process.exit(0);
}

// Run tests
runTests().catch(console.error);
EOF

# Step 6: Install Node.js dependencies
echo "📦 Step 6: Installing Node.js dependencies..."
npm install pg
npm install --save-dev @types/pg

# Step 7: Create .env file
echo "🔐 Step 7: Creating .env file..."
cat > .env << 'EOF'
# PostgreSQL Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fractality_db
DB_USER=fractality
DB_PASSWORD=cosmic_consciousness_2025

# Connection Pool
DB_MAX_CONNECTIONS=20
DB_IDLE_TIMEOUT=30000
EOF

echo ""
echo "✅ Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo "1. Run 'node test-db.js' to test your connection"
echo "2. Update the password in .env and db-config.js"
echo "3. Start building your persistence layer!"
echo ""
echo "Quick commands:"
echo "  Connect to DB: psql -U fractality -d fractality_db"
echo "  View tables: \dt consciousness.*"
echo "  View indexes: \di consciousness.*"
echo ""
echo "Happy coding! 🌌"
```