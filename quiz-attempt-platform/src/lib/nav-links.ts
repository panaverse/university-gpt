export type AllRoles = "admin" | "student" | "experienced_student" | "section_leader" | "section_leader_mentor" | "head_ta" | "instructor";

interface NavLink {
  title: string;
  href: string;
  roles: Array<AllRoles>; // Roles that can see this link
}



export const navLinks: NavLink[] = [
  {
    title: "Dashboard",
    href: "#",
    roles: [
      "admin",
      "student",
      "experienced_student",
      "section_leader",
      "section_leader_mentor",
      "head_ta",
      "instructor",
    ],
  },
  { title: "Quizzes", href: "#", roles: ["admin", "head_ta", "instructor"] },
  { title: "Progress", href: "#", roles: ["admin", "head_ta", "instructor"] },
  { title: "Settings", href: "#", roles: ["admin", "head_ta", "instructor"] },
];
