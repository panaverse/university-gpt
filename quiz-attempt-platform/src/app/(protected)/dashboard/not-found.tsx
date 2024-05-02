'use client'
import { PackageSearch } from 'lucide-react';

export default function NotFound() {
  return (
    <main className="flex h-full flex-col items-center justify-center gap-2">
      <PackageSearch className="w-10 text-gray-400" />
      <h2 className="text-xl font-semibold">Request Failed</h2>
      <button
        onClick={() => window.location.reload()}
        className="mt-4 rounded-md bg-blue-500 px-4 py-2 text-sm text-white transition-colors hover:bg-blue-400"
      >
        Refresh
      </button>
    </main>
  );
}
