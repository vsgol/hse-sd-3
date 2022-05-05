using data_lib;
using logic.Models;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace web.Pages;

public class TasksList : PageModel
{
    private readonly HwDbContext _context;
    public TasksList(HwDbContext context)
    {
        _context = context;
    }
    public IList<HwTask> Tasks { get; private set; } = new List<HwTask>();
    public void OnGet()
    {
        Tasks = _context.Tasks.Where(t => t.PublicationDate <= DateTime.Now).OrderBy(t => t.DeadlineDate).ToList();
    }
}