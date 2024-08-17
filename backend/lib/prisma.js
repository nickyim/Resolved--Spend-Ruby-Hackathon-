const { PrismaClient } = require('@prisma/client');
const { PrismaNeon } = require('@prisma/adapter-neon');
const { Pool } = require('@neondatabase/serverless');
const ws = require('ws');

const prismaClientSingleton = () => {
  const neonConfig = {
    webSocketConstructor: ws
  };
  const connectionString = process.env.DATABASE_URL;
  const pool = new Pool({ connectionString });
  const adapter = new PrismaNeon(pool);
  const prisma = new PrismaClient({ adapter });

  return prisma;
}

let prismaGlobal;

if (process.env.NODE_ENV !== 'production') {
  if (!global.prismaGlobal) {
    global.prismaGlobal = prismaClientSingleton();
  }
  prismaGlobal = global.prismaGlobal;
} else {
  prismaGlobal = prismaClientSingleton();
}

module.exports = prismaGlobal;
