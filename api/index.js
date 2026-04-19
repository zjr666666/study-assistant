import { createRequire } from "module";
const require = createRequire(import.meta.url);
const handler = require("./backend/index.py");
export default handler;
