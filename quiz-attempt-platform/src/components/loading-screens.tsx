
export default function LoadingScreenComponent() {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-gray-200 bg-opacity-50 dark:bg-gray-800 dark:bg-opacity-75 z-50">
      <div className="flex items-center space-x-2 animate-pulse">
        <div className="w-6 h-6 bg-gray-600 rounded-full dark:bg-gray-400" />
        <div className="w-6 h-6 bg-gray-600 rounded-full dark:bg-gray-400" />
        <div className="w-6 h-6 bg-gray-600 rounded-full dark:bg-gray-400" />
      </div>
    </div>
  )
}