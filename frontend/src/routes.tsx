// This will define application routes.
import { Route, Routes } from "react-router-dom";
import Landing from "./screens/Landing";
import Consent from "./screens/Consent";
import Profile from "./screens/Profile";
import SpokenQuestions from "./screens/SpokenQuestions";
import Paragraph from "./screens/Paragraph";
import Ratings from "./screens/Ratings";
import Processing from "./screens/Processing";
import RedAlarm from "./screens/RedAlarm";
import Dashboard from "./screens/Dashboard";
import ExitUnderOver from "./screens/ExitUnderOver";
import EndSession from "./screens/EndSession";
export default function AppRoutes() { return <Routes><Route path="/" element={<Landing />} /><Route path="/consent" element={<Consent />} /><Route path="/profile" element={<Profile />} /><Route path="/spoken/:id" element={<SpokenQuestions />} /><Route path="/paragraph" element={<Paragraph />} /><Route path="/ratings" element={<Ratings />} /><Route path="/processing" element={<Processing />} /><Route path="/support" element={<RedAlarm />} /><Route path="/dashboard" element={<Dashboard />} /><Route path="/exit" element={<ExitUnderOver />} /><Route path="/end" element={<EndSession />} /></Routes>; }
