export function formatTextChunk(text) {
  // Remove all instances of **
  return text.replace(/\*\*/g, "");
}
