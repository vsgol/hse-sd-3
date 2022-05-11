using data_lib;
using logic.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;

namespace web.Pages;

public class SubmissionDetails : PageModel
{
    [BindProperty]
    public Comment Comment{get; set;} = new Comment();
    
    private readonly HwDbContext _context;

    public HwTask HwTask { get; set; }
    [BindProperty]
    public Attempt Attempt{get; set;} = new Attempt();
    public IList<Comment> Comments { get; private set; } = new List<Comment>();

    public SubmissionDetails(HwDbContext context)
    {
        _context = context;
    }
    
    public async Task<IActionResult> OnGetAsync(int? id)
    {
        if (id == null)
        {
            return NotFound();
        }
        
        Attempt = await _context.Attempts.FirstOrDefaultAsync(m => m.Id == id);
        if (Attempt == null)
        {
            return NotFound();
        }
        HwTask = await _context.Tasks.FirstOrDefaultAsync(m => m.Id == Attempt.TaskId);
        Comments = _context.Comments.Where(c => c.AttemptId == Attempt.Id).ToList();
        return Page();  
    }
    
    public async Task<IActionResult> OnPostAsync(int? id)
    {
        if (id == null)
        {
            return NotFound();
        }
        
        var curAttempt = await _context.Attempts.FirstOrDefaultAsync(m => m.Id == id);

        if (curAttempt == null)
        {
            return NotFound();
        }

        curAttempt.Grade = Attempt.Grade;
        await _context.SaveChangesAsync();
        HwTask = await _context.Tasks.FirstOrDefaultAsync(m => m.Id == curAttempt.TaskId);
        Comments = _context.Comments.Where(c => c.AttemptId == curAttempt.Id).ToList();
        if (!ModelState.IsValid)
        {
            return Page();
        }

        Comment.AttemptId = Attempt.Id;
        _context.Comments.Add(Comment);
        await _context.SaveChangesAsync();
        Comment = new Comment();
        return await OnGetAsync(id);
    }
}