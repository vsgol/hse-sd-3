using data_lib;
using logic.Models;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace web.Pages;

public class SubmissionsList : PageModel
{
    private readonly HwDbContext _context;
    public SubmissionsList(HwDbContext context)
    {
        _context = context;
    }
    public IList<Attempt> Attempts { get; private set; } = new List<Attempt>();
    public IList<HwTask> Tasks { get; private set; } = new List<HwTask>();
    public void OnGet()
    {
        Attempts = _context.Attempts.OrderBy(a => a.SubmissionDate).Reverse().ToList();
        Tasks = _context.Tasks.ToList();
    }
}