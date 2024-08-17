/*
  Warnings:

  - You are about to drop the column `complaintId` on the `File` table. All the data in the column will be lost.
  - You are about to drop the `Complaint` table. If the table is not empty, all the data it contains will be lost.
  - Added the required column `entryId` to the `File` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "File" DROP CONSTRAINT "File_complaintId_fkey";

-- AlterTable
ALTER TABLE "File" DROP COLUMN "complaintId",
ADD COLUMN     "entryId" INTEGER NOT NULL;

-- DropTable
DROP TABLE "Complaint";

-- CreateTable
CREATE TABLE "Entry" (
    "id" SERIAL NOT NULL,
    "entryId" TEXT NOT NULL,
    "isComplaint" BOOLEAN NOT NULL,
    "product" TEXT,
    "subProduct" TEXT,
    "issue" TEXT,
    "subIssue" TEXT,
    "entryText" TEXT NOT NULL,
    "summary" TEXT,
    "dateSentToCompany" TIMESTAMP(3),
    "dateReceived" TIMESTAMP(3),
    "company" TEXT,
    "companyResponse" TEXT,
    "companyPublicResponse" TEXT,
    "consumerDisputed" TEXT,
    "consumerConsentProvided" TEXT,
    "state" TEXT,
    "zipCode" TEXT,
    "submittedVia" TEXT,
    "tags" TEXT,
    "timely" BOOLEAN,
    "productCategory" TEXT,
    "subProductCategory" TEXT,
    "vectorId" TEXT,

    CONSTRAINT "Entry_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Entry_entryId_key" ON "Entry"("entryId");

-- AddForeignKey
ALTER TABLE "File" ADD CONSTRAINT "File_entryId_fkey" FOREIGN KEY ("entryId") REFERENCES "Entry"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
