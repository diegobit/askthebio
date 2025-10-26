const defaultPersonaName = "Diego Giorgini";

const personaName = import.meta.env.VITE_PERSON_NAME || defaultPersonaName;
const personaFirstName =
  personaName.trim().split(/\s+/)[0] || defaultPersonaName.split(" ")[0];

export const appConfig = {
  personaName,
  personaFirstName,
  title: `AskTheBio of ${personaName}`,
  description: `Chat with ${personaName}'s personal AI - trained on their knowledge, experiences, and thoughts. Ask anything about ${personaName}.`,
};
