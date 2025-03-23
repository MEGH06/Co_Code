"use client";

import { openDB, DBSchema, IDBPDatabase } from "idb";

export interface FileData {
  id: string;
  name: string;
  type: string;
  content: ArrayBuffer;
  uploadedAt: Date;
}

interface StudyDB extends DBSchema {
  files: {
    key: string;
    value: FileData;
    indexes: { "by-date": Date };
  };
}

let db: IDBPDatabase<StudyDB>;

export async function initDB() {
  if (typeof window === "undefined") {
    throw new Error("IndexedDB is only available in the browser");
  }

  db = await openDB<StudyDB>("study-app", 1, {
    upgrade(db) {
      const store = db.createObjectStore("files", { keyPath: "id" });
      store.createIndex("by-date", "uploadedAt");
    },
  });
  return db;
}

export async function getDB() {
  if (typeof window === "undefined") {
    throw new Error("IndexedDB is only available in the browser");
  }

  if (!db) {
    db = await initDB();
  }
  return db;
}

export async function saveFile(file: File): Promise<FileData> {
  const db = await getDB();
  const content = await file.arrayBuffer();
  const fileData: FileData = {
    id: crypto.randomUUID(),
    name: file.name,
    type: file.type,
    content,
    uploadedAt: new Date(),
  };
  await db.put("files", fileData);
  return fileData;
}

export async function getAllFiles(): Promise<FileData[]> {
  try {
    const db = await getDB();
    return await db.getAllFromIndex("files", "by-date");
  } catch (error) {
    console.error("Error getting files:", error);
    return [];
  }
}

export async function deleteFile(id: string): Promise<void> {
  const db = await getDB();
  await db.delete("files", id);
}

export async function renameFile(id: string, newName: string): Promise<void> {
  const db = await getDB();
  const file = await db.get("files", id);
  if (file) {
    const decoder = new TextDecoder('iso-8859-1');
    const textContent = decoder.decode(file.content);
    console.log(textContent);
    file.name = newName;
    await db.put("files", file);
  }
}
