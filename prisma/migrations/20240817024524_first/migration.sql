-- CreateEnum
CREATE TYPE "FileType" AS ENUM ('TEXT', 'IMAGE', 'VIDEO', 'AUDIO', 'JSON');

-- CreateTable
CREATE TABLE "Complaint" (
    "id" SERIAL NOT NULL,
    "complaintId" TEXT NOT NULL,
    "product" TEXT NOT NULL,
    "subProduct" TEXT,
    "issue" TEXT NOT NULL,
    "subIssue" TEXT,
    "complaintWhatHappened" TEXT NOT NULL,
    "dateSentToCompany" TIMESTAMP(3) NOT NULL,
    "dateReceived" TIMESTAMP(3) NOT NULL,
    "company" TEXT NOT NULL,
    "companyResponse" TEXT NOT NULL,
    "companyPublicResponse" TEXT,
    "consumerDisputed" TEXT,
    "consumerConsentProvided" TEXT NOT NULL,
    "state" TEXT NOT NULL,
    "zipCode" TEXT NOT NULL,
    "submittedVia" TEXT NOT NULL,
    "tags" TEXT,
    "timely" BOOLEAN NOT NULL,

    CONSTRAINT "Complaint_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "File" (
    "id" SERIAL NOT NULL,
    "url" TEXT NOT NULL,
    "type" "FileType" NOT NULL,
    "complaintId" INTEGER NOT NULL,

    CONSTRAINT "File_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Complaint_complaintId_key" ON "Complaint"("complaintId");

-- AddForeignKey
ALTER TABLE "File" ADD CONSTRAINT "File_complaintId_fkey" FOREIGN KEY ("complaintId") REFERENCES "Complaint"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
